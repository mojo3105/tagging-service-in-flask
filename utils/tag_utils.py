"""
The script contains utility functions for tags.
"""

#imports
from redis import Redis
from datetime import date, datetime


def create_redis_client():   
    """
    The function will create redis client
    :param: None
    :return redis_client: redis client object 
    """
    redis_client = Redis(host='redis-flask', port=6379, db=0)
    return redis_client


def update_tags(stock, current_price):
    """
    The function will update tags values in stock tables when current_price of stock changed.
    :param stock: stock object
    :param current_price: current price of stock
    :return stock: stock object with updated values for tags and current_price
    """
    if current_price > stock.current_price:
        if (stock.ATH is None) and (stock.WH_52 is None) and (stock.ATL is None) and (stock.WL_52 is None):
            stock.WH_52 = current_price
            stock.ATH = current_price
            stock.WL_52 = stock.current_price
            stock.ATL = stock.current_price
            stock.ATH_updated_at = datetime.now()
            stock.WH_52_updated_at = datetime.now()
            stock.ATL_updated_at = datetime.now()
            stock.WL_52_updated_at = datetime.now()
        if current_price > stock.ATH:
            stock.ATH = current_price
            stock.WH_52 = current_price
            stock.ATH_updated_at = datetime.now()
            stock.WH_52_updated_at = datetime.now()
        elif current_price > stock.WH_52:
            stock.WH_52 = current_price
            stock.WH_52_updated_at = datetime.now()
    else:
        if (stock.ATL is None) and (stock.WL_52 is None) and (stock.ATH is None) and (stock.WH_52 is None):
            stock.WL_52 = current_price
            stock.ATL = current_price
            stock.WH_52 = stock.current_price
            stock.ATH = stock.current_price
            stock.ATL_updated_at = datetime.now()
            stock.WL_52_updated_at = datetime.now()
            stock.ATH_updated_at = datetime.now()
            stock.WH_52_updated_at = datetime.now()
        if current_price < stock.ATL:
            stock.ATL = current_price
            stock.WL_52 = current_price
            stock.ATL_updated_at = datetime.now()
            stock.WL_52_updated_at = datetime.now()
        elif current_price < stock.WL_52:
            stock.WL_52 = current_price
            stock.WL_52_updated_at = datetime.now()

    stock.current_price = current_price
    return stock


def update_redis_values(stock):
    """
    The function will update tags values stored in redis.
    :param stock: stock object containing stock data
    :return: None
    """
    today_date = date.today().strftime("%d%m%Y")
    tag_name_list = ['WH_52', 'WL_52', 'ATH', 'ATL']
    redis_client = create_redis_client()
    for tags in tag_name_list:
        key = f'{tags}_{today_date}'
        if eval(f'stock.{tags}_updated_at').date().strftime("%d%m%Y") == today_date:
            if redis_client.exists(key):
                values = redis_client.lrange(key, 0, -1)
                if stock.stock_symbol.encode() not in values:
                    redis_client.rpush(key, stock.stock_symbol)
            else:
                value = [stock.stock_symbol]
                redis_client.rpush(key, *value)
        values = redis_client.lrange(key, 0, -1)
        print(key, values)


def get_tags_data(tag, result_data, stock=None):
    """
    The function will fetch the data for tag from redis and will append in result_data list.
    :param tag: name of tag
    :param stock: name of stock
    :param result_data: dictionary containing tag data results
    :return: None
    """
    today_date = date.today().strftime("%d%m%Y")
    key = f'{tag}_{today_date}'
    redis_client = create_redis_client()
    if redis_client.exists(key):
        values = redis_client.lrange(key, 0, -1)
        values = [value.decode() for value in values]
        if stock:
            if (stock in values) and (stock in result_data.keys()):
                result_data[stock].append(tag)
            elif (stock in values) and (stock not in result_data.keys()):
                result_data[stock] = [tag]
            elif (stock not in values) and (stock in result_data.keys()):
                pass
            else:
                result_data[stock] = []
        else:
            result_data[tag] = values
    else:
        result_data[tag] = []
