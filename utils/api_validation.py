"""
The script contain code to validate api requests.
"""

#imports
from cerberus import Validator
from constants.common import ValidatorSchema, APIConstant


def stocks_validation(request_data):
    """
    The function will perform validation of stocks api request data.
    :param request_data: dictionary containing api request data
    :return request_data: dictionary with validated api request data 
    :return msg: error message if any
    """
    try:
        msg = None
        v = Validator()
        schema = ValidatorSchema.STOCK_VALIDATION_SCHEMA
        if not v.validate(request_data, schema):
            msg = v.errors
            return None, msg
        
        request_data['company_name'] = request_data['company_name'].strip()
        request_data['stock_symbol'] = request_data['stock_symbol'].strip().upper()

        if request_data['company_name'] == "":
            msg = APIConstant.INVALID_VALUE_ERROR.format(field="company_name")
            return None, msg
        
        if request_data['stock_symbol'] == "":
            msg = APIConstant.INVALID_VALUE_ERROR.format(field="stock_symbol")
            return None, msg

        return request_data, msg
    
    except KeyError as e:
        msg = APIConstant.KEY_INCORRECT_MESSAGE.format(e=e)
        return None, msg
    
    except Exception as e:
        msg = APIConstant.COMMON_ERROR.format(e=e)
        return None, msg
    

def tags_validation(request_data):
    """
    The function will perform tags api request data.
    :param request_data: dictionary with request data
    :return request_data: dictionary with validated request data
    :return msg: error message if any
    """
    try:
        msg = None
        v = Validator()
        schema = ValidatorSchema.TAG_VALIDATION_SCHEMA
        if not v.validate(request_data, schema):
            msg = v.errors
            return None, msg

        return request_data, msg
    
    except KeyError as e:
        msg = APIConstant.KEY_INCORRECT_MESSAGE.format(e=e)
        return None, msg
    
    except Exception as e:
        msg = APIConstant.COMMON_ERROR.format(e=e)
        return None, msg