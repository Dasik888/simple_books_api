import json
import random

import requests

from methods.api_methods import ApiMethods
from methods.base_methods import BaseMethods
from settings import *


class TestOrders:

    # Positive checks

    def test_submit_an_order(self):
        books_id_list = ApiMethods().get_list_of_all_available_books_id()
        book_id = random.choice(books_id_list)
        url = BASE_URL + ORDERS_LIST
        headers = {'Authorization': 'Bearer {}'.format(REGISTRED_USER_TOKEN), 'Content-Type': 'application/json'}
        body = {"bookId": book_id, "customerName": USER_NAME}
        response = requests.post(url, headers=headers, data=json.dumps(body))
        assert response.status_code == 201, f"Status code is incorrect: {response.status_code}"
        BaseMethods().assert_list_not_null(response=response)
        assert response.json()['created'], f"Order is not created: {response.json()['created']}"

    def test_get_all_user_orders_list(self):
        ApiMethods().delete_all_user_orders()
        ApiMethods().submit_an_order()
        url = BASE_URL + ORDERS_LIST
        headers = {'Authorization': 'Bearer {}'.format(REGISTRED_USER_TOKEN)}
        response = requests.get(url, headers=headers)
        assert response.status_code == 200, f"Status code is incorrect: {response.status_code}"
        BaseMethods().assert_list_not_null(response=response)
        BaseMethods().validate_response_get_orders_list(response=response)
        assert len(response.json()) == 1, 'Order number is not correct'

    def test_get_order_information(self):
        ApiMethods().delete_all_user_orders()
        order_id = ApiMethods().submit_an_order()
        url = BASE_URL + ORDERS_LIST + f'/{order_id}'
        headers = {'Authorization': 'Bearer {}'.format(REGISTRED_USER_TOKEN)}
        response = requests.get(url, headers=headers)
        assert response.status_code == 200, f"Status code is incorrect: {response.status_code}"
        BaseMethods().assert_list_not_null(response=response)
        BaseMethods().validate_response_get_single_order(response=response)
        assert response.json()['id'] == order_id, f"Returned order id is not correct: {response.json()['id']}"

    def test_update_an_order(self):
        ApiMethods().delete_all_user_orders()
        order_id = ApiMethods().submit_an_order()
        expected_customer_name = 'John'
        url = BASE_URL + ORDERS_LIST + f'/{order_id}'
        headers = {'Authorization': 'Bearer {}'.format(REGISTRED_USER_TOKEN), 'Content-Type': 'application/json'}
        body = {"customerName": expected_customer_name}
        response = requests.patch(url, headers=headers, data=json.dumps(body))
        assert response.status_code == 204, f"Status code is incorrect: {response.status_code}"
        new_customer_name = ApiMethods().get_order_information(order_id)['customerName']
        assert new_customer_name == expected_customer_name, 'Order is not updated'

    def test_delete_an_order(self):
        ApiMethods().delete_all_user_orders()
        order_id = ApiMethods().submit_an_order()
        initial_number_of_orders = ApiMethods().get_number_of_user_orders()
        url = BASE_URL + ORDERS_LIST + f'/{order_id}'
        headers = {'Authorization': 'Bearer {}'.format(REGISTRED_USER_TOKEN)}
        response = requests.delete(url, headers=headers)
        assert response.status_code == 204, f"Status code is incorrect: {response.status_code}"
        number_of_orders_after_delete = ApiMethods().get_number_of_user_orders()
        assert initial_number_of_orders == 1 + number_of_orders_after_delete, 'Order is not deleted'

    # Negative checks

    def test_submit_an_order_with_invalid_token(self):
        books_id_list = ApiMethods().get_list_of_all_available_books_id()
        book_id = random.choice(books_id_list)
        url = BASE_URL + ORDERS_LIST
        headers = {'Authorization': 'Bearer {}'.format(INVALID_USER_TOKEN), 'Content-Type': 'application/json'}
        body = {"bookId": book_id, "customerName": USER_NAME}
        response = requests.post(url, headers=headers, data=json.dumps(body))
        assert response.status_code == 401, f"Status code is incorrect: {response.status_code}"
        assert response.text == '{"error":"Invalid bearer token."}', f"Error text is incorrect: {response.text}"

    def test_delete_an_order_with_invalid_token(self):
        ApiMethods().delete_all_user_orders()
        order_id = ApiMethods().submit_an_order()
        initial_number_of_orders = ApiMethods().get_number_of_user_orders()
        url = BASE_URL + ORDERS_LIST + f'/{order_id}'
        headers = {'Authorization': 'Bearer {}'.format(INVALID_USER_TOKEN)}
        response = requests.delete(url, headers=headers)
        assert response.status_code == 401, f"Status code is incorrect: {response.status_code}"
        assert response.text == '{"error":"Invalid bearer token."}', f"Error text is incorrect: {response.text}"
        number_of_orders_after_delete = ApiMethods().get_number_of_user_orders()
        assert initial_number_of_orders == number_of_orders_after_delete, 'Order is not deleted'

    def test_get_order_information_with_invalid_token(self):
        ApiMethods().delete_all_user_orders()
        order_id = ApiMethods().submit_an_order()
        url = BASE_URL + ORDERS_LIST + f'/{order_id}'
        headers = {'Authorization': 'Bearer {}'.format(INVALID_USER_TOKEN)}
        response = requests.get(url, headers=headers)
        assert response.status_code == 401, f"Status code is incorrect: {response.status_code}"
        assert response.text == '{"error":"Invalid bearer token."}', f"Error text is incorrect: {response.text}"
