import json
import random
import requests

from methods.base_methods import BaseMethods
from settings import *


class ApiMethods:

    def get_list_of_all_available_books_id(self):
        books_id_list = []
        url = BASE_URL + BOOKS_LIST
        response = requests.get(url)
        assert response.status_code == 200, f"Status code is incorrect: {response.status_code}"
        BaseMethods().assert_list_not_null(response=response)
        for books in response.json():
            if books['available'] == True:
                books_id_list.append(books['id'])
        return books_id_list

    def get_list_of_all_books_id(self):
        books_id_list = []
        url = BASE_URL + BOOKS_LIST
        response = requests.get(url)
        assert response.status_code == 200, f"Status code is incorrect: {response.status_code}"
        BaseMethods().assert_list_not_null(response=response)
        for books in response.json():
            books_id_list.append(books['id'])
        return books_id_list

    def submit_an_order(self):
        books_id_list = self.get_list_of_all_available_books_id()
        book_id = random.choice(books_id_list)
        url = BASE_URL + ORDERS_LIST
        headers = {'Authorization': 'Bearer {}'.format(REGISTRED_USER_TOKEN), 'Content-Type': 'application/json'}
        body = {"bookId": book_id, "customerName": USER_NAME}
        response = requests.post(url, headers=headers, data=json.dumps(body))
        assert response.status_code == 201, f"Status code is incorrect: {response.status_code}"
        BaseMethods().assert_list_not_null(response=response)
        return response.json()['orderId']

    def get_number_of_user_orders(self):
        url = BASE_URL + ORDERS_LIST
        headers = {'Authorization': 'Bearer {}'.format(REGISTRED_USER_TOKEN)}
        response = requests.get(url, headers=headers)
        assert response.status_code == 200, f"Status code is incorrect: {response.status_code}"
        return len(response.json())

    def get_user_orders_list(self):
        url = BASE_URL + ORDERS_LIST
        headers = {'Authorization': 'Bearer {}'.format(REGISTRED_USER_TOKEN)}
        response = requests.get(url, headers=headers)
        assert response.status_code == 200, f"Status code is incorrect: {response.status_code}"
        return response.json()

    def delete_an_order(self, order_id):
        url = BASE_URL + ORDERS_LIST + f'/{order_id}'
        headers = {'Authorization': 'Bearer {}'.format(REGISTRED_USER_TOKEN)}
        response = requests.delete(url, headers=headers)
        assert response.status_code == 204, f"Status code is incorrect: {response.status_code}"

    def delete_all_user_orders(self):
        orders_list = self.get_user_orders_list()
        if orders_list:
            for orders in orders_list:
                self.delete_an_order(orders['id'])
        assert len(self.get_user_orders_list()) == 0, 'Not all orders are deleted'

    def get_order_information(self, order_id):
        url = BASE_URL + ORDERS_LIST + f'/{order_id}'
        headers = {'Authorization': 'Bearer {}'.format(REGISTRED_USER_TOKEN)}
        response = requests.get(url, headers=headers)
        assert response.status_code == 200, f"Status code is incorrect: {response.status_code}"
        BaseMethods().assert_list_not_null(response=response)
        BaseMethods().validate_response_get_single_order(response=response)
        return response.json()
