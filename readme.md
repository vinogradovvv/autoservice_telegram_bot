# Telegram car service simple crm.

Telegram bot providing functionality of crm system to manage the work of a BMW car service.
Includes VIN decoding, parts searching in original parts catalog, and ordering parts through Euroauto company.

## Installation

    git clone https://github.com/vinogradovvv/autoservice_telegram_bot.git
    cd autoservice_telegram_bot
    pip install -r requirements.txt

## Configuring
    
    DEMO mode:
        Copy .env.template file to .env and fill it with parameters:
            - BOT_DEMO - True for demo mode / False for real mode.
            - BOT_TOKEN - Telegram bot token got from BotFather.
            - EUROAUTO_LOGIN - opt.euroauto.ru account login.
            - EUROAUTO_PASSWORD - opt.euroauto.ru account password.
        **If Euroauto account is empty, bot will not display buttons of Euroauto ineracting.**
    
    REAL mode:
        Switch bot mode to real mode with BOT_DEMO=False in .env file.
        Fill the crew.json file with users information saving json syntax:
            for every user:
                - id must be changed to telegram user id
                - name must be changed to user name
                - role must be changed to user job position

## DEMO and REAL modes
    DEMO mode provides user an ability to test functionality of any role.
    In REAL mode user's set of awailable actions depends on user group, described in crew.json file.
    Automatic reminding workers of the new work awailable only in REAL mode.
