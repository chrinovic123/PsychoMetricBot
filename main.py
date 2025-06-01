import logging
import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)
from psy import big_five, mbti, depression, anxiety

# Configuration du logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Charge les variables d'environnement
load_dotenv()

# Dictionnaire pour suivre l'état des utilisateurs
user_states = {}

# Message de démarrage personnalisé
START_MESSAGE = """
🌟 *Bienvenue sur PsychoTest Bot* 🌟

Je suis un assistant psychologique qui vous propose plusieurs tests validés scientifiquement :

🔹 *Tests de personnalité* :
- /mbti - Test MBTI (16 personnalités)
- /bigfive - Test des 5 grands traits (OCEAN)

🔹 *Tests d'auto-évaluation* :
- /depression - Test PHQ-9 (dépression)
- /anxiety - Test GAD-7 (anxiété)

📌 Utilisez les commandes ci-dessus ou le menu interactif pour commencer un test.

ℹ Pour plus d'informations : /help
"""

# Message d'aide détaillé
HELP_MESSAGE = """
🆘 *Aide - PsychoTest Bot* 🆘

*Commandes disponibles* :

🔹 *Tests de personnalité* :
- /mbti - Test de typologie MBTI (16 personnalités)
- /bigfive - Test des 5 grands traits de personnalité (OCEAN)

🔹 *Tests de santé mentale* :
- /depression - Test PHQ-9 (évaluation des symptômes dépressifs)
- /anxiety - Test GAD-7 (évaluation des symptômes anxieux)

🔹 *Autres commandes* :
- /start - Redémarrer le bot
- /help - Afficher ce message
- /cancel - Annuler un test en cours

📝 *Note importante* : 
Les résultats fournis sont indicatifs et ne constituent pas un diagnostic médical. En cas de doute, consultez un professionnel de santé.

💡 Conseil : Complétez plusieurs tests pour une meilleure compréhension de vous-même.
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Message de démarrage avec menu interactif."""
    user = update.effective_user
    keyboard = [
        [
            InlineKeyboardButton("🧠 Test MBTI", callback_data='mbti'),
            InlineKeyboardButton("🌊 Big Five", callback_data='big_five'),
        ],
        [
            InlineKeyboardButton("😔 Test Dépression", callback_data='depression'),
            InlineKeyboardButton("😰 Test Anxiété", callback_data='anxiety'),
        ],
        [
            InlineKeyboardButton("ℹ Aide", callback_data='help'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Gestion à la fois des commandes et des callbacks
    if update.message:
        await update.message.reply_text(
            START_MESSAGE,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    elif update.callback_query:
        await update.callback_query.message.edit_text(
            START_MESSAGE,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    else:
        logger.warning("Update n'a ni message ni callback_query")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Affiche le message d'aide détaillé."""
    await update.message.reply_text(
        HELP_MESSAGE,
        parse_mode='Markdown'
    )

async def start_mbti(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Commande pour démarrer directement le test MBTI."""
    user_id = update.effective_user.id
    user_states[user_id] = {
        'current_test': 'mbti',
        'current_question': 0,
        'responses': [],
        'test_started': True
    }
    await send_question(update, context, user_id)

async def start_big_five(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Commande pour démarrer directement le test Big Five."""
    user_id = update.effective_user.id
    user_states[user_id] = {
        'current_test': 'big_five',
        'current_question': 0,
        'responses': [],
        'test_started': True
    }
    await send_question(update, context, user_id)

async def start_depression(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Commande pour démarrer directement le test PHQ-9."""
    user_id = update.effective_user.id
    user_states[user_id] = {
        'current_test': 'depression',
        'current_question': 0,
        'responses': [],
        'test_started': True
    }
    await send_question(update, context, user_id)

async def start_anxiety(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Commande pour démarrer directement le test GAD-7."""
    user_id = update.effective_user.id
    user_states[user_id] = {
        'current_test': 'anxiety',
        'current_question': 0,
        'responses': [],
        'test_started': True
    }
    await send_question(update, context, user_id)

async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int) -> None:
    """Envoie la question actuelle à l'utilisateur."""
    user_state = user_states[user_id]
    test_name = user_state['current_test']
    question_index = user_state['current_question']
    
    # Récupérer les questions en fonction du test choisi
    if test_name == 'mbti':
        questions = mbti.questions
    elif test_name == 'big_five':
        questions = big_five.questions
    elif test_name == 'depression':
        questions = depression.questions
    elif test_name == 'anxiety':
        questions = anxiety.questions
    else:
        return
    
    # Vérifier si le test est terminé
    if question_index >= len(questions):
        await show_results(update, context, user_id)
        return
    
    question_text, options = questions[question_index]
    
    # Créer des boutons pour les options de réponse
    keyboard = []
    for i, option in enumerate(options):
        keyboard.append([InlineKeyboardButton(option, callback_data=f'answer_{i}')])
    
    # Ajouter un bouton Annuler
    keyboard.append([InlineKeyboardButton("❌ Annuler le test", callback_data='cancel_test')])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Envoyer la question
    if update.callback_query:
        await update.callback_query.edit_message_text(
            text=f"*Question {question_index + 1}/{len(questions)}*:\n\n{question_text}",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    else:
        await context.bot.send_message(
            chat_id=user_id,
            text=f"*Question {question_index + 1}/{len(questions)}*:\n\n{question_text}",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Traite la réponse de l'utilisateur."""
    query = update.callback_query
    await query.answer()
    
    # Gestion de l'annulation
    if query.data == 'cancel_test':
        await cancel(update, context)
        return
    
    user_id = query.from_user.id
    if user_id not in user_states or not user_states[user_id]['test_started']:
        return
    
    # Extraire l'index de la réponse
    answer_index = int(query.data.split('_')[1])
    user_states[user_id]['responses'].append(answer_index)
    user_states[user_id]['current_question'] += 1
    
    # Envoyer la question suivante
    await send_question(update, context, user_id)

async def show_results(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int) -> None:
    """Affiche les résultats du test."""
    user_state = user_states[user_id]
    test_name = user_state['current_test']
    responses = user_state['responses']
    
    # Calculer les résultats
    if test_name == 'mbti':
        result = mbti.calculate_result(responses)
    elif test_name == 'big_five':
        result = big_five.calculate_result(responses)
    elif test_name == 'depression':
        result = depression.calculate_result(responses)
    elif test_name == 'anxiety':
        result = anxiety.calculate_result(responses)
    else:
        result = "Erreur: test inconnu"
    
    # Envoyer les résultats
    if update.callback_query:
        await update.callback_query.edit_message_text(
            text=result,
            parse_mode='Markdown'
        )
    else:
        await context.bot.send_message(
            chat_id=user_id,
            text=result,
            parse_mode='Markdown'
        )
    
    # Proposer de faire un autre test
    keyboard = [
        [InlineKeyboardButton("🔹 Faire un autre test", callback_data='new_test')],
        [InlineKeyboardButton("🏠 Menu principal", callback_data='start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await context.bot.send_message(
        chat_id=user_id,
        text="Que souhaitez-vous faire maintenant ?",
        reply_markup=reply_markup
    )
    
    # Réinitialiser l'état de l'utilisateur
    del user_states[user_id]

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Annule le test en cours."""
    user_id = update.effective_user.id
    if user_id in user_states:
        del user_states[user_id]
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            text="❌ Test annulé. Que souhaitez-vous faire ?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🏠 Menu principal", callback_data='start')],
                [InlineKeyboardButton("ℹ Aide", callback_data='help')]
            ])
        )
    else:
        await update.message.reply_text(
            "❌ Test annulé. Utilisez /start pour recommencer ou /help pour voir les options."
        )

async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Gère les actions du menu principal."""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'start':
        await show_main_menu(update, context)
    elif query.data == 'help':
        await help_command(update, context)
    elif query.data == 'new_test':
        await show_main_menu(update, context)

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Affiche le menu principal (version compatible callback et commande)"""
    user = update.effective_user
    keyboard = [
        [
            InlineKeyboardButton("🧠 Test MBTI", callback_data='mbti'),
            InlineKeyboardButton("🌊 Big Five", callback_data='big_five'),
        ],
        [
            InlineKeyboardButton("😔 Test Dépression", callback_data='depression'),
            InlineKeyboardButton("😰 Test Anxiété", callback_data='anxiety'),
        ],
        [
            InlineKeyboardButton("ℹ Aide", callback_data='help'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = f"Bonjour {user.first_name}!\n" + START_MESSAGE
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            text=text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

def main() -> None:
    """Lance le bot."""
    # Récupère le token depuis les variables d'environnement
    token = os.getenv('TELEGRAM_TOKEN')
    if not token:
        raise ValueError("Le token Telegram n'a pas été trouvé dans les variables d'environnement")
    
    # Crée l'application
    application = ApplicationBuilder().token(token).build()
    
    # Ajoute les handlers de commande
    application.add_handler(CommandHandler("start", show_main_menu))
    application.add_handler(CallbackQueryHandler(show_main_menu, pattern='^start$'))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("cancel", cancel))
    application.add_handler(CommandHandler("mbti", start_mbti))
    application.add_handler(CommandHandler("bigfive", start_big_five))
    application.add_handler(CommandHandler("depression", start_depression))
    application.add_handler(CommandHandler("anxiety", start_anxiety))
    
    # Handlers pour les callbacks
    application.add_handler(CallbackQueryHandler(start_mbti, pattern='^mbti$'))
    application.add_handler(CallbackQueryHandler(start_big_five, pattern='^big_five$'))
    application.add_handler(CallbackQueryHandler(start_depression, pattern='^depression$'))
    application.add_handler(CallbackQueryHandler(start_anxiety, pattern='^anxiety$'))
    application.add_handler(CallbackQueryHandler(handle_answer, pattern='^answer_'))
    application.add_handler(CallbackQueryHandler(handle_menu, pattern='^(start|help|new_test)$'))
    application.add_handler(CallbackQueryHandler(cancel, pattern='^cancel_test$'))
    
    # Lance le bot
    application.run_polling()

if __name__ == '__main__':
    main()