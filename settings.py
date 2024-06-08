import os
from typing import Dict
from copy import copy
from dotenv import load_dotenv, set_key, find_dotenv
from pydantic import SecretStr, StrictStr
from pydantic_settings import BaseSettings

dotenv_file = find_dotenv()
load_dotenv(dotenv_file, override=True)


class BotSettings(BaseSettings):
    """
    Telegram bot settings.
    """
    bot_token: SecretStr = os.getenv("BOT_TOKEN", None)
    bot_demo: bool = os.getenv("BOT_DEMO", True)


class DecoderSettings(BaseSettings):
    """
    BMW decoder settings.
    """
    url_head: StrictStr = os.getenv("DECODER_URL_HEAD", None)
    url_tail: StrictStr = os.getenv("DECODER_URL_TAIL", None)


class EuroautoSettings(BaseSettings):
    """
    Euroauto settings
    """
    stores: StrictStr = os.getenv("EUROAUTO_SPB_STORES")
    my_stores: StrictStr = os.getenv("EUROAUTO_MY_STORES")
    url: StrictStr = os.getenv("EUROAUTO_URL", None)
    login: SecretStr = os.getenv("EUROAUTO_LOGIN", None)
    password: SecretStr = os.getenv("EUROAUTO_PASSWORD", None)
    token: SecretStr = os.getenv("EUROAUTO_TOKEN", None)
    token_exp: StrictStr = os.getenv("EUROAUTO_TOKEN_EXP", '1')

    auth_headers: Dict = {'Content-Type': 'application/x-www-form-urlencoded',
                          'Accept': 'application/json'}
    auth_data: Dict = {'login': login,
                       'password': password}
    headers: Dict = copy(auth_headers)
    headers['Authorization'] = f'Bearer {token}'

    # @staticmethod
    def new_token(self, token: str, token_exp: str) -> None:
        """
        Methode saves new auth token, and token exp timestamp to .env file
        :param token: new auth token
        :param token_exp: new token exp timestamp
        """
        os.environ["EUROAUTO_TOKEN"] = token
        os.environ["EUROAUTO_TOKEN_EXP"] = token_exp
        set_key(dotenv_file, "EUROAUTO_TOKEN", os.environ["EUROAUTO_TOKEN"])
        set_key(dotenv_file, "EUROAUTO_TOKEN_EXP", os.environ["EUROAUTO_TOKEN_EXP"])
        self.token_exp = token_exp
        self.headers['Authorization'] = f'Bearer {token}'
