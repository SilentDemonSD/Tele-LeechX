from random import choice

from TeleLX import BOT_THEME, USER_THEMES, LOGGER
from TeleLX.coreyyyy.bot_theme.themes import fx_optimised, fx_minimal

AVAILABLE_THEMES = {'fx-optimised-theme': fx_optimised, 'fx-minimal-theme': fx_minimal}

def BotTheme(user_id_):

    theme_ = USER_THEMES.get(str(user_id_), BOT_THEME)
    if theme_ in AVAILABLE_THEMES.keys():
        return (AVAILABLE_THEMES.get(theme_)).TXStyle()
    if theme_ == "fx-random-theme":
        rantheme = choice(list(AVAILABLE_THEMES.values()))
        LOGGER.info(f"Random Theme Choosen : {rantheme}")
        return rantheme.TXStyle()
    return fx_optimised.TXStyle()

