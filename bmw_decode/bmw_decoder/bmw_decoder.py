"""
BMW decoder allows user to decode vin codes and part numbers,
and provides catalog link
"""
import re
import requests
from typing import Dict, Tuple, Optional
from settings import DecoderSettings


def _get_car_page(vin: str) -> Tuple[Optional[str], str]:
    """
    Function makes post request with car's VIN code.
    If VIN ok returns text of response and link to catalog
    for this car, else returns None and catalog start page
    :param vin: last 7 symbols of VIN code
    :return: catalog page for car if VIN ok / None, and link to catalog page
    """
    decoder_settings = DecoderSettings()
    url_head = decoder_settings.url_head
    url_tail = decoder_settings.url_tail
    params = {'vin': vin}

    with requests.session() as web_session:
        response = web_session.post(f'{url_head}{url_tail}', params=params)
        link = response.text
        if vin in response.text:
            catalog_link = f'{url_head}{link}'
            car_info = web_session.get(catalog_link).text
        else:
            catalog_link = url_head
            car_info = None

        return car_info, catalog_link


def _get_part_page(part_number: str) -> str:
    """
    Function makes get request with part's number,
    and returns catalog part's page
    :param part_number: part number in catalog
    :return: catalog page for part with given part number
    """
    url = f'https://cats.parts/${part_number}'

    with requests.session() as web_session:
        part_info = web_session.get(url)
        return part_info.text


def _decode_vin(vin: str) -> Dict:
    """
    Function parse response and return dict of cars info if VIN was right,
    and dict with just catalog link if VIN was wrong.
    :param vin: last 7 symbols of VIN code
    :return: dict with car info
    """
    car_info, catalog_link = _get_car_page(vin)
    if car_info:
        body_code = re.search(r"(\. )(.+?)(\. )", car_info).group(2)
        data_strings = re.findall(r'(etk-mospid-carinfo-value">)(.+?)(</)', car_info)
        model = data_strings[0][1]
        body_type = data_strings[3][1]
        release_date = data_strings[4][1]
        region = data_strings[2][1][98:]
        car_data = {'body_code': body_code,
                    'model': model,
                    'body_type': body_type,
                    'release_date': release_date,
                    'region': region,
                    'catalog_link': catalog_link}
    else:
        car_data = {'catalog_link': catalog_link}
    return car_data


def _decode_part_number(part_number: str) -> Optional[str]:
    """
    Function parse response and return part name
    or None if part number was not decode
    :param part_number: part number in catalog/None
    :return: part name in catalog
    """
    part_info = _get_part_page(part_number)
    try:
        part_name = re.search(r'("part-number-name">)(.+?)(</)', part_info).group(2)
        return part_name
    except AttributeError:
        return None


def _get_catalog() -> str:
    """
    Function returns catalog start page link.
    :return: catalog start page link
    """
    decoder_settings = DecoderSettings()
    return decoder_settings.url_head


class BmwDecoder:
    """
    Class with methods of decoding VIN codes and part numbers
    """
    @staticmethod
    def decode_vin():
        """
        Methode to use decoding vin code function
        """
        return _decode_vin

    @staticmethod
    def decode_part_number():
        """
        Methode to use decoding part number function
        """
        return _decode_part_number

    @staticmethod
    def get_catalog():
        """
        Methode to get catalog link
        """
        return _get_catalog()


if __name__ == "__main__":
    _get_car_page()
    _get_part_page()
    _decode_vin()
    _decode_part_number()
    _get_catalog()
    BmwDecoder()
