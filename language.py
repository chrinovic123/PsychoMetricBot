import json
import os
import logging

# Configure logging
logger = logging.getLogger(__name__)

_translations = {}
_default_lang = 'en'
_current_lang = _default_lang

def load_language(lang_code: str) -> bool:
    """
    Loads a language file into the cache.
    Constructs the file path (e.g., locales/{lang_code}.json).
    If it exists and is not already in _translations, loads the JSON file.
    Returns True if loaded successfully or already in cache, False otherwise.
    """
    if lang_code in _translations:
        return True

    file_path = os.path.join('locales', f'{lang_code}.json')

    if not os.path.exists(file_path):
        logger.warning(f"Language file not found: {file_path}")
        return False

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            _translations[lang_code] = json.load(f)
        logger.info(f"Successfully loaded language: {lang_code}")
        return True
    except FileNotFoundError:
        logger.error(f"Error: Language file not found at {file_path} (should have been caught by os.path.exists).")
        return False
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from language file: {file_path}")
        return False
    except Exception as e:
        logger.error(f"An unexpected error occurred while loading {file_path}: {e}")
        return False

def set_language(lang_code: str) -> bool:
    """
    Sets the active language for the system.
    Returns True if the language is supported and loaded, False otherwise.
    """
    global _current_lang
    if load_language(lang_code):
        _current_lang = lang_code
        logger.info(f"Current language set to: {lang_code}")
        return True
    else:
        logger.warning(f"Failed to set language to {lang_code}. It might not be supported or loadable.")
        # Optionally, revert to default if setting new one fails and current is invalid
        if _current_lang not in _translations:
             _current_lang = _default_lang
             logger.info(f"Reverted current language to default: {_default_lang}")
        return False

def get_current_language() -> str:
    """Returns the currently set language code."""
    return _current_lang

def get_string(key: str, lang: str = None, **kwargs) -> str:
    """
    Retrieves a translated string by its key.
    - key: The key for the string (e.g., 'main.start_message').
    - lang: Optional language code to override the current language.
    - kwargs: Values for placeholder substitution in the string.
    Returns the translated (and formatted) string, or a fallback message.
    """
    target_lang = lang if lang else _current_lang

    # Ensure the target language is loaded
    if target_lang not in _translations:
        if not load_language(target_lang):
            logger.warning(f"Target language '{target_lang}' could not be loaded for key '{key}'. Attempting fallback.")
            # Fallback to default language if target language failed to load
            if _default_lang not in _translations:
                load_language(_default_lang) # Try to load default if not already loaded

            if _default_lang in _translations:
                target_lang = _default_lang
                logger.info(f"Using default language '{_default_lang}' as fallback for key '{key}'.")
            else:
                # This case means even default language is not available.
                return f"Missing translation resources for key: {key} (Lang: {target_lang})"


    keys = key.split('.')
    current_dict_level = _translations.get(target_lang, {})

    try:
        for k_part in keys:
            if isinstance(current_dict_level, list):
                try:
                    k_part = int(k_part)
                    current_dict_level = current_dict_level[k_part]
                except (ValueError, IndexError):
                    raise KeyError(f"Invalid index '{k_part}' for list key part in '{key}'")
            elif isinstance(current_dict_level, dict):
                current_dict_level = current_dict_level[k_part]
            else: # Should not happen if JSON is structured correctly
                raise KeyError(f"Expected dict or list, got {type(current_dict_level)} at '{k_part}' in key '{key}'")

        retrieved_string = current_dict_level

        if not isinstance(retrieved_string, str):
            logger.warning(f"Key '{key}' in lang '{target_lang}' did not resolve to a string, but to {type(retrieved_string)}. Returning as is.")
            return str(retrieved_string)

        if kwargs:
            return retrieved_string.format(**kwargs)
        return retrieved_string

    except (KeyError, IndexError) as e:
        logger.debug(f"Key '{key}' not found in language '{target_lang}' (Error: {e}). Attempting fallback to default language.")
        # Fallback to default language if key not found in target_lang
        if target_lang != _default_lang and _default_lang in _translations:
            try:
                current_dict_level = _translations[_default_lang]
                for k_part in keys:
                    if isinstance(current_dict_level, list):
                        k_part = int(k_part)
                        current_dict_level = current_dict_level[k_part]
                    else:
                        current_dict_level = current_dict_level[k_part]

                retrieved_string = current_dict_level
                if not isinstance(retrieved_string, str):
                     logger.warning(f"Key '{key}' (fallback '{_default_lang}') did not resolve to a string, but to {type(retrieved_string)}. Returning as is.")
                     return str(retrieved_string)

                if kwargs:
                    return retrieved_string.format(**kwargs)
                return retrieved_string
            except (KeyError, IndexError, ValueError):
                logger.error(f"Key '{key}' also not found in default language '{_default_lang}'.")
                return f"Missing translation for: {key} (Lang: {target_lang}, Fallback: {_default_lang})"
            except Exception as ex_fallback:
                logger.error(f"Unexpected error during fallback for key '{key}': {ex_fallback}")
                return f"Error during fallback for: {key}"

        logger.error(f"Key '{key}' not found in language '{target_lang}' and no fallback possible or fallback failed.")
        return f"Missing translation for: {key} (Lang: {target_lang})"
    except Exception as ex_main:
        logger.error(f"An unexpected error occurred while retrieving key '{key}': {ex_main}")
        return f"Error retrieving: {key}"


# Pre-load default and French languages at startup
load_language('en')
load_language('fr')

# Example usage (for testing, can be removed later)
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO) # Enable logging for example

    print("\n--- Testing French ---")
    set_language('fr')
    print(f"Current lang: {get_current_language()}")
    print(f"Start message (fr): {get_string('main.start_message')}")
    print(f"MBTI Q1 (fr): {get_string('mbti.questions.0.question')}")

    print("\n--- Testing English ---")
    set_language('en')
    print(f"Current lang: {get_current_language()}")
    print(f"Start message (en): {get_string('main.start_message')}")
    print(f"MBTI Q1 (en): {get_string('mbti.questions.0.question')}")

    print("\n--- Testing Fallback and Missing Keys ---")
    # Assuming 'es.json' doesn't exist and 'main.non_existent_key' doesn't exist in en or fr
    print(f"Non-existent key: {get_string('main.non_existent_key')}")
    # This will try 'es', then fallback to 'en' (default) for 'main.start_message'
    print(f"Start message (es, fallback to en): {get_string('main.start_message', lang='es')}")
    # This will try 'es', then fallback to 'en' (default) for 'main.non_existent_key'
    print(f"Non-existent key (es, fallback to en): {get_string('main.non_existent_key_for_es', lang='es')}")

    print("\n--- Testing Formatting ---")
    # Ensure 'main.greeting' exists in your en.json and fr.json
    # e.g., "greeting": "Hello {name}!" in en.json
    # e.g., "greeting": "Bonjour {name}!" in fr.json
    print(f"Greeting (en): {get_string('main.greeting', name='Jules', lang='en')}")
    print(f"Greeting (fr): {get_string('main.greeting', name='Jules', lang='fr')}")

    print("\n--- Testing direct key to list/dict (should return as string representation) ---")
    print(f"MBTI questions object (fr): {get_string('mbti.questions', lang='fr')}")

    print("\n--- Testing invalid index in key ---")
    print(f"MBTI invalid Q index (fr): {get_string('mbti.questions.99.question', lang='fr')}")

    print("\n--- Testing with a language that will fail to load initially and then set_language ---")
    if not os.path.exists('locales/xx.json'): # Ensure it doesn't exist
        print(f"String for non-existent lang 'xx': {get_string('main.start_message', lang='xx')}")
        print(f"Current lang after failed attempt: {get_current_language()}")

        print("Setting language to 'xx' (expected to fail but set_language might revert to default or keep previous valid):")
        set_language_result = set_language('xx')
        print(f"set_language('xx') result: {set_language_result}")
        print(f"Current lang after set_language('xx'): {get_current_language()}")
        print(f"Start message (current lang after failed set): {get_string('main.start_message')}")

    print("\n--- Test loading a language that exists but is not pre-loaded ---")
    # Create a dummy es.json for this test
    if not os.path.exists('locales/es.json'):
        with open('locales/es.json', 'w', encoding='utf-8') as f_es:
            json.dump({"main": {"start_message": "Hola Mundo"}}, f_es)
        print("Dummy 'locales/es.json' created for testing.")

    print(f"Start message (es, first time): {get_string('main.start_message', lang='es')}")
    set_language('es')
    print(f"Start message (es, after set_language): {get_string('main.start_message')}")

    # Clean up dummy file
    if os.path.exists('locales/es.json') and "Hola Mundo" in open('locales/es.json').read():
        os.remove('locales/es.json')
        print("Dummy 'locales/es.json' removed.")

    print("\n--- Test get_string for a key that exists only in default lang ---")
    # Add a key to en.json that is not in fr.json
    # For example, add "only_in_default": "This exists only in English." to "main" in en.json
    # _translations['en']['main']['only_in_default'] = "This exists only in English." # Simulate
    # Make sure 'fr' is current language
    set_language('fr')
    # print(f"String only in default (current fr): {get_string('main.only_in_default')}")
    # del _translations['en']['main']['only_in_default'] # cleanup simulation
    print("Skipping 'only_in_default' test as it requires modifying live files or more complex mocking not suited for this context.")

    print("\nExample usage finished.")
```
