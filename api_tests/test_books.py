import random
import pytest
import requests

from methods.api_methods import ApiMethods
from methods.base_methods import BaseMethods
from settings import *


class TestBooks:

    # Positive checks

    def test_get_list_of_all_books(self):
        url = BASE_URL + BOOKS_LIST
        response = requests.get(url)
        assert response.status_code == 200, f"Status code is incorrect: {response.status_code}"
        BaseMethods().assert_list_not_null(response=response)
        BaseMethods().validate_response_get_books_list(response=response)

    def test_get_list_of_fiction_books(self):
        url = BASE_URL + BOOKS_LIST
        params = {"type": "fiction"}
        response = requests.get(url, headers=HEADERS, params=params)
        assert response.status_code == 200, f"Status code is incorrect: {response.status_code}"
        BaseMethods().assert_list_not_null(response=response)
        BaseMethods().validate_response_get_books_list(response=response)
        for books in response.json():
            assert books['type'] == 'fiction', f"Returned books type not fiction: {books['type']}"

    def test_get_list_of_non_fiction_books(self):
        url = BASE_URL + BOOKS_LIST
        params = {"type": "non-fiction"}
        response = requests.get(url, headers=HEADERS, params=params)
        assert response.status_code == 200, f"Status code is incorrect: {response.status_code}"
        BaseMethods().assert_list_not_null(response=response)
        BaseMethods().validate_response_get_books_list(response=response)
        for books in response.json():
            assert books['type'] == 'non-fiction', f"Returned books type not non-fiction: {books['type']}"

    @pytest.mark.parametrize("limit", [1, 5]) # limit can be from 1 to 20
    def test_get_list_of_books_with_limit(self, limit):
        url = BASE_URL + BOOKS_LIST
        params = {"limit": limit}
        response = requests.get(url, headers=HEADERS, params=params)
        assert response.status_code == 200, f"Status code is incorrect: {response.status_code}"
        BaseMethods().assert_list_not_null(response=response)
        BaseMethods().validate_response_get_books_list(response=response)
        assert len(response.json()) == limit, f"Returned books limit is not correct: {len(response.json())}"

    def test_get_single_book_information(self):
        books_id_list = ApiMethods().get_list_of_all_books_id()
        book_id = random.choice(books_id_list)
        url = BASE_URL + BOOKS_LIST + f'/{book_id}'
        response = requests.get(url)
        assert response.status_code == 200, f"Status code is incorrect: {response.status_code}"
        BaseMethods().assert_list_not_null(response=response)
        BaseMethods().validate_response_get_single_book(response=response)
        assert response.json()['id'] == book_id, f"Returned books id is not correct: {response.json()['id']}"

    # Negative checks

    def test_get_book_information_with_nonexistent_id(self):
        book_id = 50
        url = BASE_URL + BOOKS_LIST + f'/{book_id}'
        response = requests.get(url)
        assert response.status_code == 404, f"Status code is incorrect: {response.status_code}"
        assert response.text == '{"error":"No book with id 50"}', f"Error text is incorrect: {response.text}"

    def test_get_list_of_books_over_limit(self):
        url = BASE_URL + BOOKS_LIST
        params = {"limit": 21}
        response = requests.get(url, headers=HEADERS, params=params)
        assert response.status_code == 400, f"Status code is incorrect: {response.status_code}"
        assert response.text == """{"error":"Invalid value for query parameter 'limit'. Cannot be greater than 20."}"""\
            , f"Error text is incorrect: {response.text}"

    def test_get_list_of_books_with_invalid_type(self):
        url = BASE_URL + BOOKS_LIST
        params = {"type": 1}
        response = requests.get(url, headers=HEADERS, params=params)
        assert response.status_code == 400, f"Status code is incorrect: {response.status_code}"
        assert response.text == """{"error":"Invalid value for query parameter 'type'. Must be one of: fiction, non-fiction."}""",\
            f"Error text is incorrect: {response.text}"
