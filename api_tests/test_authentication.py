import json
import requests

from methods.base_methods import BaseMethods
from settings import *


class TestAuthentication:

    # Positive checks

    def test_check_api_status(self):
        url = BASE_URL + API_STATUS
        response = requests.get(url)
        assert response.status_code == 200, f"Status code is incorrect: {response.status_code}"
        assert response.text == '{"status":"OK"}', f"Error text is incorrect: {response.text}"

    def test_register_new_api_user(self):
        email = BaseMethods().add_timestamp_to_email(USER_EMAIL)
        url = BASE_URL + NEW_USER
        body = {"clientName": USER_NAME, "clientEmail": email}
        response = requests.post(url, headers=HEADERS, data=json.dumps(body))
        assert response.status_code == 201, f"Status code is incorrect: {response.status_code}"
        BaseMethods().assert_list_not_null(response=response)
        token = response.json()["accessToken"]
        print('User get token: ' + token)
        BaseMethods().assert_token_not_empty(token)

    # Negative checks
    # TODO need to add negative check for expired token (can be added in 7 days after registration a user)

    def test_register_existed_api_user(self):
        url = BASE_URL + NEW_USER
        body = {"clientName": USER_NAME, "clientEmail": USER_EMAIL}
        response = requests.post(url, headers=HEADERS, data=json.dumps(body))
        assert response.status_code == 409, f"Status code is incorrect: {response.status_code}"
        assert response.text == '{"error":"API client already registered. Try a different email."}',\
            f"Error text is incorrect: {response.text}"

    def test_register_user_without_data(self):
        url = BASE_URL + NEW_USER
        body = {"clientName": '', "clientEmail": ''}
        response = requests.post(url, headers=HEADERS, data=json.dumps(body))
        assert response.status_code == 400, f"Status code is incorrect: {response.status_code}"
        assert response.text == '{"error":"Invalid or missing client name."}', \
            f"Error text is incorrect: {response.text}"

    def test_register_user_with_invalid_email(self):
        url = BASE_URL + NEW_USER
        body = {"clientName": USER_NAME, "clientEmail": INVALID_USER_EMAIL}
        response = requests.post(url, headers=HEADERS, data=json.dumps(body))
        assert response.status_code == 400, f"Status code is incorrect: {response.status_code}"
        assert response.text == '{"error":"Invalid or missing client email."}', \
            f"Error text is incorrect: {response.text}"
