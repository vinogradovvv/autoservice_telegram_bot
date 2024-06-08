"""
Euroauto API interface provides user the set of methods
to interact with Euroauto through API
"""
import requests
from typing import Dict, Callable
from datetime import datetime
from settings import EuroautoSettings

euroauto = EuroautoSettings()


def _make_get_response(url: str,
                       headers: Dict,
                       params: Dict = None,
                       timeout: int = 10,
                       success: int = 200) -> requests.Response | int:
    """
    Function makes GET request with given url, headers, params
    :param url: requests url
    :param headers: requests headers
    :param params: requests params
    :param timeout: requests timeout in sec
    :param success: success status code
    :return: response object if request was success, and status code if was not
    """
    with requests.session() as web_session:
        if params:
            response = web_session.get(
                url=url,
                headers=headers,
                params=params,
                timeout=timeout
            )
        else:
            response = web_session.get(
                url=url,
                headers=headers,
                timeout=timeout
            )
    status_code = response.status_code
    if status_code == success:
        return response
    return status_code


def _make_post_response(url: str,
                        data: Dict,
                        headers: Dict,
                        timeout: int = 10,
                        success: int = 200) -> requests.Response | int:
    """
    Function makes POST request with given url, data, headers
    :param url: requests url
    :param data: requests data
    :param headers: requests headers
    :param timeout: requests timeout in sec
    :param success: success status code
    :return: response object if request was success, and status code if was not.
    """
    with requests.session() as web_session:
        response = web_session.post(
            url=url,
            data=data,
            headers=headers,
            timeout=timeout
        )
    status_code = response.status_code
    if status_code == success:
        return response
    return status_code


def _make_delete_response(url: str,
                          headers: Dict,
                          params: Dict = None,
                          timeout: int = 10,
                          success: int = 200) -> requests.Response | int:
    """
    Function makes DELETE request with given url, headers, params
    :param url: requests url
    :param headers: requests headers
    :param params: requests params
    :param timeout: requests timeout in sec
    :param success: success status code
    :return: response object if request was success, and status code if was not
    """
    with requests.session() as web_session:
        if params:
            response = web_session.delete(
                url=url,
                headers=headers,
                params=params,
                timeout=timeout
            )
        else:
            response = web_session.delete(
                url=url,
                headers=headers,
                timeout=timeout
            )
    status_code = response.status_code
    if status_code == success:
        return response
    return status_code


def _get_new_token(url: str,
                   data: Dict,
                   headers: Dict,
                   func: Callable = _make_post_response) -> Dict | int:
    """
    Function gets new auth token with POST request to API endpoint
    :param url: API url
    :param data: requests data
    :param headers: requests headers
    :param func: POST request function
    :return: serialised response if request was success, or requests status code if was not
    """
    endpoint = '/auth'
    url = url + endpoint
    response = func(url=url, data=data, headers=headers)
    if isinstance(response, requests.Response):
        response = response.json()
    return response


def _check_token() -> None:
    """
    Function check if existing auth token expired, and if it is gets new token, and expiration timestamp.
    Then saves it to .env file with settings class methode.
    :return: None
    """
    if datetime.now() > datetime.utcfromtimestamp(int(euroauto.token_exp)):
        response = _get_new_token(euroauto.url, euroauto.auth_data, euroauto.auth_headers)
        token = response['data']['token']
        token_exp = str(response['data']['expires'])
        euroauto.new_token(token, token_exp)
    return None


def _find_products(partnumber: str, func: Callable = _make_get_response) -> Dict | int:
    """
    Function makes Get request to API with given partnumber and returns info about part and replacements in stock.
    :param partnumber: catalog partnumber
    :param func: GET request function
    :return: serialised response if request was success, or requests status code if was not
    """
    endpoint = '/offers/products/manufacturers/3/new'
    url = euroauto.url + endpoint
    params = {'code': partnumber, 'replacements': 'true'}
    response = func(url=url, headers=euroauto.headers, params=params)
    if isinstance(response, requests.Response):
        response = response.json()
    return response


def _find_offers(product_code: str, func: Callable = _make_get_response) -> Dict | int:
    """
    Function makes Get request to API with given product code,
    and returns info about offers of product from euroauto shops and warehouses
    :param product_code: euroauto product code
    :param func: GET request function
    :return: serialised response if request was success, or requests status code if was not
    """
    endpoint = f'/offers/products/{product_code}'
    url = euroauto.url + endpoint
    response = func(url=url, headers=euroauto.headers)
    if isinstance(response, requests.Response):
        response = response.json()
    return response


def _add_to_cart(offer_id: str, quantity: int, func: Callable = _make_post_response) -> Dict | int:
    """
    Function adds to euroauto cart given quantity of offer product
    :param offer_id: euroauto offer id
    :param quantity: amount of parts
    :param func: POST request function
    :return: serialised response if request was success, or requests status code if was not
    """
    endpoint = f'/carts/offers/{offer_id}'
    url = euroauto.url + endpoint
    data = {'labels[API]': 'telegram_bot',
            'quantity': quantity}
    response = func(url=url, data=data, headers=euroauto.headers)
    if isinstance(response, requests.Response):
        response = response.json()
    return response


def _list_cart(func: Callable = _make_get_response) -> Dict | int:
    """
    Function lists euroauto cart
    :param func: GET request function
    :return: serialised response if request was success, or requests status code if was not
    """
    endpoint = '/carts/items'
    url = euroauto.url + endpoint
    params = {'labels[API]': 'telegram_bot'}
    response = func(url=url, params=params, headers=euroauto.headers)
    if isinstance(response, requests.Response):
        response = response.json()
    return response


def _remove_item(offer_id: str, func: Callable = _make_delete_response) -> Dict | int:
    """
    Function removes an item with given offer id from euroauto cart
    :param offer_id: euroauto offer id
    :param func: DELETE request function
    :return: serialised response if request was success, or requests status code if was not
    """
    endpoint = f'/carts/offers/{offer_id}'
    url = euroauto.url + endpoint
    params = {'labels[API]': 'telegram_bot'}
    response = func(url=url, params=params, headers=euroauto.headers)
    if isinstance(response, requests.Response):
        response = response.json()
    return response


def _delete_cart(func: Callable = _make_delete_response) -> Dict | int:
    """
    Function removes euroauto cart
    :param func: DELETE request function
    :return: serialised response if request was success, or requests status code if was not
    """
    endpoint = '/carts'
    url = euroauto.url + endpoint
    params = {'labels[API]': 'telegram_bot'}
    response = func(url=url, params=params, headers=euroauto.headers)
    if isinstance(response, requests.Response):
        response = response.json()
    return response


class EuroautoApiInterface:
    """
    Euroauto API interface class with methods to work with API
    """

    @staticmethod
    def get_new_token():
        """
        Method updates euroauto auth token
        """
        return _get_new_token

    @staticmethod
    def check_token():
        """
        Method checks if available token is still valid
        """
        return _check_token

    @staticmethod
    def find_products():
        """
        Methode finds products in the Euroauto
        """
        return _find_products

    @staticmethod
    def find_offers():
        """
        Methode finds offers in the Euroauto
        """
        return _find_offers

    @staticmethod
    def add_to_cart():
        """
        Method adds an item to the Euroauto cart
        """
        return _add_to_cart

    @staticmethod
    def list_cart():
        """
        Method lists the Euroauto cart
        """
        return _list_cart

    @staticmethod
    def remove_item():
        """
        Method removes an item from the Euroauto cart
        """
        return _remove_item

    @staticmethod
    def delete_cart():
        """
        Method removes the Euroauto cart
        """
        return _delete_cart


if __name__ == "__main__":
    _make_get_response()
    _make_post_response()
    _get_new_token()
    _check_token()
    _find_products()
    _find_offers()
    _add_to_cart()
    _list_cart()
    _remove_item()
    _delete_cart()

    EuroautoApiInterface()
