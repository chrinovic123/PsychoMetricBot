<p align="center">
  <h1 align="center">PsychoTest Bot</h1>
</p>
<p align="center">
  <a href="https://www.gnu.org/licenses/gpl-3.0"><img src="https://img.shields.io/badge/License-GPLv3-blue.svg" alt="License: GPL v3"></a>
  <img src="https://img.shields.io/badge/python-3.9%2B-blue.svg" alt="Python 3.9+">
</p>

PsychoTest Bot is a Telegram bot that provides users with access to various psychological assessments.

## Available Tests

The bot currently offers the following assessments:

*   **MBTI (Myers-Briggs Type Indicator):** A personality inventory designed to identify a person's personality type, strengths, and preferences.
*   **Big Five (OCEAN Model):** A personality test that measures five broad dimensions of personality: Openness, Conscientiousness, Extraversion, Agreeableness, and Neuroticism.
*   **PHQ-9 (Patient Health Questionnaire-9):** A self-administered questionnaire used for screening, diagnosing, monitoring, and measuring the severity of depression.
*   **GAD-7 (Generalized Anxiety Disorder 7-item scale):** A self-administered questionnaire used for screening and measuring the severity of generalized anxiety disorder.

## How to Use

You can interact with PsychoTest Bot using commands or by clicking the inline keyboard buttons presented by the bot.

A short GIF or video demonstrating the bot in action would be a great addition here!
<!-- TODO: Add a GIF or video demonstrating the bot in action -->

### Commands

*   `/start`: Initializes the bot and displays the main menu.
*   `/help`: Shows a help message with a list of available commands and information about the tests.
*   `/cancel`: Cancels any ongoing test.
*   `/mbti`: Starts the MBTI personality test.
*   `/bigfive`: Starts the Big Five personality test.
*   `/depression`: Starts the PHQ-9 depression screening test.
*   `/anxiety`: Starts the GAD-7 anxiety screening test.

## Setup and Local Execution

To run PsychoTest Bot locally, follow these steps:

### Prerequisites

*   Python 3.x
*   A Telegram Bot Token (obtain this by talking to the [BotFather](https://t.me/botfather) on Telegram)

### Installation

1.  **Clone the repository (if you haven't already):**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1.  Create a file named `.env` in the root directory of the project.
2.  Add your Telegram Bot Token to this file:
    ```env
    TELEGRAM_TOKEN='YOUR_TELEGRAM_BOT_TOKEN'
    ```
    Replace `YOUR_TELEGRAM_BOT_TOKEN` with your actual token.

### Running the Bot

Once the setup is complete, you can run the bot using:

```bash
python main.py
```

The bot will start polling for updates from Telegram.

## Technology Stack

This project is built using the following technologies:

*   **Python:** The core programming language.
*   **python-telegram-bot:** A library for interacting with the Telegram Bot API.

## Contributing

Contributions are welcome! If you have suggestions for improvements or want to contribute code, please follow these steps:

### Reporting Bugs

*   Ensure the bug was not already reported by searching on GitHub under Issues.
*   If you're unable to find an open issue addressing the problem, open a new one. Be sure to include a title and clear description, as much relevant information as possible, and a code sample or an executable test case demonstrating the expected behavior that is not occurring.

### Suggesting Enhancements

*   Open an issue with the label `enhancement`.
*   Clearly describe the enhancement and the motivation for it.

### Pull Request Process

1.  Fork the repo and create your branch from `main` (or the default branch).
2.  Add tests for your changes.
3.  Ensure your code lints.
4.  Issue that pull request!

## Disclaimer

The psychological tests provided by this bot are for informational and educational purposes only. They are not intended to be a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition. Never disregard professional medical advice or delay in seeking it because of something you have read or interpreted from the results of these tests.

## License

This project is licensed under the GPL-0.3. See the [LICENSE](LICENSE) file for details.
