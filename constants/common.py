"""
The script contains constants to use for generic purpose.
"""

class APIConstant:
    DEFAULT_MESSAGE_NAME = "Error"
    SUCCESS_MESSAGE_NAME = "Success"
    ALLOWED_METHODS_DEFAULT = ['GET', 'POST']
    ALLOWED_METHODS_ALL = ['GET', 'POST', 'PUT', 'DELETE']
    COMMON_ERROR = "An Error occured {e}!"
    VALID_TAG_ERROR = "Please provide valid tag!"
    NOT_FOUND_ERROR = "{model} not found!"
    PROVIDE_ID_ERROR = "Please provide {model} id in url path!"
    COMMON_SUCCESS_MESSAGE = "{model} successfully {action}!"
    TAG_NAMES_LIST = ['WH_52', 'WL_52', 'ATH', 'ATL']
    TAG_VALUE_ERROR = "Please provide valid tag!"
    KEY_INCORRECT_MESSAGE = "Please provide correct field {e}!"
    INVALID_VALUE_ERROR = "Provide correct not null and non empty field {field}!"
    INVALID_INPUT = "Please provide correct input!"


class ValidatorSchema:
    STOCK_VALIDATION_SCHEMA = {
        'company_name': {
            'type': 'string',
            'required': True
        },
        'stock_symbol': {
            'type': 'string',
            'required': True
        },
        'current_price': {
            'type': ['integer', 'float'],
            'min': 1,
            'required': True
        }
    }
    TAG_VALIDATION_SCHEMA = {
        "tag" : {
            'type': 'string',
        },
        "stock" : {
            'type': 'string',
        }
    }