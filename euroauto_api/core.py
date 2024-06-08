"""
Euroauto API core file
"""
from settings import EuroautoSettings
from euroauto_api.utils.api_handler import EuroautoApiInterface

euroauto = EuroautoSettings()
euroauto_api = EuroautoApiInterface()

if __name__ == "__main__":
    EuroautoApiInterface()
