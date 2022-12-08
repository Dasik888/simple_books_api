import time
import jsonschema

from json_schema import JsonSchema


class BaseMethods:

    def add_timestamp_to_email(self, email):
        timestamp = str(self.get_timestamp_in_millisecond())
        email = email.split("@")
        email = email[0] + f"+{timestamp}@" + email[1]
        print('generated email: ', email)
        return email

    def get_timestamp_in_millisecond(self):
        return round(time.time() * 1000)

    def assert_list_not_null(self, response):
        assert response.json(), "Response not contains list: " + str(response.text)

    def assert_token_not_empty(self, token):
        assert len(token) != 0, "Response is empty"

    def validate_response_get_books_list(self, response):
        jsonschema.validate(response.json(), JsonSchema.get_books_list)

    def validate_response_get_single_book(self, response):
        jsonschema.validate(response.json(), JsonSchema.get_single_book)

    def validate_response_get_orders_list(self, response):
        jsonschema.validate(response.json(), JsonSchema.get_orders_list)

    def validate_response_get_single_order(self, response):
        jsonschema.validate(response.json(), JsonSchema.get_single_order)
