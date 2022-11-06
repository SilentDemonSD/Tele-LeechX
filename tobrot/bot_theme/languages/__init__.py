from tobrot import LOGGER
from tobrot.bot_theme.languages import en, bn

AVAILABLE_LANG = {'english': en, 'bengali': bn}
BOT_LANG = "English"

def BotLang():

    if BOT_LANG.lower() in AVAILABLE_LANG.keys():
        return (AVAILABLE_LANG.get(BOT_LANG)).TXLanguage()
    else:
        return en.TXLanguage()
