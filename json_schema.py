class JsonSchema:
    get_books_list = {
      "type": "array",
      "properties": {
        "id": {
          "type": "integer"
        },
        "name": {
          "type": "string"
        },
        "type": {
          "type": "string"
        },
        "available": {
          "type": "boolean"
        }
      },
      "required": [
        "id",
        "name",
        "type",
        "available"
      ]
    }

    get_single_book = {
      "type": "object",
      "properties": {
        "author": {
          "type": "string"
        },
        "available": {
          "type": "boolean"
        },
        "current-stock": {
          "type": "integer"
        },
        "id": {
          "type": "integer"
        },
        "name": {
          "type": "string"
        },
        "price": {
          "type": "number"
        },
        "type": {
          "type": "string"
        }
      },
      "required": [
        "author",
        "available",
        "current-stock",
        "id",
        "name",
        "price",
        "type"
      ]
    }

    get_orders_list = {
      "type": "array",
      "properties": {
        "id": {
          "type": "string"
        },
        "bookId": {
          "type": "integer"
        },
        "customerName": {
          "type": "string"
        },
        "createdBy": {
          "type": "string"
        },
        "quantity": {
          "type": "integer"
        },
        "timestamp": {
          "type": "integer"
        }
      },
      "required": [
        "id",
        "bookId",
        "customerName",
        "createdBy",
        "quantity",
        "timestamp"
      ]
    }

    get_single_order = {
      "type": "object",
      "properties": {
        "id": {
          "type": "string"
        },
        "bookId": {
          "type": "integer"
        },
        "customerName": {
          "type": "string"
        },
        "createdBy": {
          "type": "string"
        },
        "quantity": {
          "type": "integer"
        },
        "timestamp": {
          "type": "integer"
        }
      },
      "required": [
        "id",
        "bookId",
        "customerName",
        "createdBy",
        "quantity",
        "timestamp"
      ]
    }
