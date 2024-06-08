"""
telegram bot core file
"""
from telegram import __version__ as tg_ver
from settings import BotSettings
from telegram.ext import Application
from telegram_api.handlers.start import start_handler
from telegram_api.handlers.role_choice import role_choice_handler
from telegram_api.handlers.new_car import add_car_handler
from telegram_api.handlers.check_current_cars import check_current_cars
from telegram_api.handlers.history_search import history_search
from telegram_api.handlers.exit import exit_handler
from telegram_api.handlers.error import error
from telegram_api.handlers.help import help_handler


try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"Your PTB version {tg_ver} is not compatible. It must be 20.0.0 or above."
    )

bot_settings = BotSettings()
bot_token = bot_settings.bot_token.get_secret_value()
bot_demo = bot_settings.bot_demo
application = Application.builder().token(bot_token).build()

application.add_handler(start_handler)
if bot_demo:
    application.add_handler(role_choice_handler)
application.add_handler(add_car_handler)
application.add_handler(check_current_cars)
application.add_handler(history_search)
application.add_handler(exit_handler)
application.add_handler(help_handler)
application.add_error_handler(error)

if __name__ == "main":
    pass
