"""
The script contains code to initialize the flask application.
"""

#imports
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config.config import set_configs
from datetime import datetime
from utils.tag_utils import get_tags_data, update_tags
from utils.api_validation import stocks_validation, tags_validation
from constants.common import APIConstant

#creating flask application instance
app = Flask(__name__)

#setting configurations for database
app = set_configs(app)

#creatingn database instance for app
db = SQLAlchemy(app)

#migrate instance to migrate changes 
migrate = Migrate(app, db)

#model
class Stocks(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    company_name = db.Column(db.String(100))
    stock_symbol = db.Column(db.String(50), unique = True)
    current_price = db.Column(db.Numeric(precision=10, scale=2))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    WH_52 = db.Column(db.Numeric(precision=10, scale=2), default=None)
    WH_52_updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    WL_52 = db.Column(db.Numeric(precision=10, scale=2), default=None)
    WL_52_updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    ATH = db.Column(db.Numeric(precision=10, scale=2), default=None)
    ATH_updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    ATL = db.Column(db.Numeric(precision=10, scale=2), default=None)
    ATL_updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __init__(self, company_name, stock_symbol, current_price):
        self.company_name = company_name
        self.stock_symbol = stock_symbol
        self.current_price = current_price


    def serialize(self):
        return {
            'id': self.id,
            'company_name': self.company_name,
            'stock_symbol': self.stock_symbol,
            'current_price': self.current_price,
            'created_at': self.created_at,
            'WH_52': self.WH_52,
            'WH_52_updated_at': self.WH_52_updated_at,
            'WL_52': self.WL_52,
            'WL_52_updated_at': self.WL_52_updated_at,
            'ATH': self.ATH,
            'ATH_updated_at': self.ATH_updated_at,
            'ATL': self.ATL,
            'ATL_updated_at': self.ATL_updated_at
        }

    def serialize_for_fluctuation(self):
        return {
            'stock': self.stock_symbol,
            'current_price': self.current_price
        }

  
#routes
@app.route('/stocks/', methods=APIConstant.ALLOWED_METHODS_DEFAULT)
@app.route('/stocks/<int:id>/', methods=APIConstant.ALLOWED_METHODS_DEFAULT)
def stocks_route(id=None):
    """
    The function will handle request for route stocks
    :param id: id of stock if provided in path
    :return: json response containing either data/message depending upon request type and errors if any and status 
              code
    """
    msg_name = APIConstant.DEFAULT_MESSAGE_NAME
    if request.method == 'GET':
        try:
            if id:
                stock = Stocks.query.get(id)
                if stock:
                    serialized_data = stock.serialize()
                else:
                    msg_value = APIConstant.NOT_FOUND_ERROR.format(model="Stock")
                    serialized_data = {msg_name:msg_value}
            else:
                stocks_data = Stocks.query.all()
                serialized_data = list(map(lambda stock: stock.serialize(), stocks_data))
        except Exception as e:
            msg_value = APIConstant.COMMON_ERROR.format(e=e)
            serialized_data = {msg_name:msg_value}
        finally:
            return jsonify(serialized_data), 200

    if request.method == 'POST':
        try:
            request_data, msg = stocks_validation(request_data=request.json)
            if msg:
                msg_value = msg
            else:
                stock = Stocks(company_name=request_data['company_name'], stock_symbol=request_data['stock_symbol'], 
                               current_price=request_data['current_price'])
                db.session.add(stock)
                db.session.commit()
                msg_name = APIConstant.SUCCESS_MESSAGE_NAME
                msg_value = APIConstant.COMMON_SUCCESS_MESSAGE.format(model="Stock", action="added")
        except Exception as e:
            msg_value = APIConstant.COMMON_ERROR.format(e=e)
        finally:
            return jsonify({msg_name:msg_value}), 201


    if request.method == 'PUT':
        try:
            if not id:
                msg_value = APIConstant.PROVIDE_ID_ERROR.format(model="Stock")
            else:
                stock = Stocks.query.get(id)
                if stock:
                    request_data, msg = stocks_validation(request_data=request.json)
                    if msg:
                        msg_value = msg
                    else:
                        if request_data['company_name'] != stock.company_name:
                            stock.company_name = request_data['company_name']
                        if request_data['stock_symbol'] != stock.stock_symbol:
                            stock.stock_symbol != request_data['stock_symbol']
                        if request_data['current_price'] != stock.current_price:
                            stock = update_tags(stock, request_data['current_price'])
                        db.session.commit()
                        msg_name = APIConstant.SUCCESS_MESSAGE_NAME
                        msg_value = APIConstant.COMMON_SUCCESS_MESSAGE.format(model="Stock", action="updated")
                else:
                    msg_value = APIConstant.NOT_FOUND_ERROR.format(model="Stock")
        except Exception as e:
            msg_value = APIConstant.COMMON_ERROR.format(e=e)
        finally:
            return jsonify({msg_name:msg_value}), 200

    if request.method == 'DELETE':
        try:
            if not id:
                msg_value = APIConstant.PROVIDE_ID_ERROR.format(model="Stock")
            else:
                stock = Stocks.query.get(id)
                if stock:
                    db.session.delete(stock)
                    db.session.commit()
                    msg_name = APIConstant.SUCCESS_MESSAGE_NAME
                    msg_value = APIConstant.COMMON_SUCCESS_MESSAGE.format(model="Stock", action='deleted')
                else:
                    msg_value = APIConstant.NOT_FOUND_ERROR.format(model="Stock")
        except Exception as e:
            msg_value = APIConstant.COMMON_ERROR.format(e=e)
        finally:
            return jsonify({msg_name:msg_value}), 200


#routes
@app.route('/tags/')
def tags_route():
    """
    The function will handle requests for route tags.
    :param tag: name of tag if provided in path
    :return: json response containing either data/message depending upon request type and errors if any and status 
              code
    """
    if request.method == 'GET':
        msg_name = APIConstant.DEFAULT_MESSAGE_NAME
        stocks_list = [stock.stock_symbol for stock in Stocks.query.all()]
        tags_list = APIConstant.TAG_NAMES_LIST
        result_data = {}
        try:
            request_data, msg = tags_validation(request_data=request.json)
            if msg:
                result_data[msg_name] = msg
            else:
                if ['stock'] == list(request_data.keys()):
                    if request_data['stock'] == "":
                        for stock in stocks_list:
                            for tag in tags_list:
                                get_tags_data(tag, result_data, stock=stock)
                    elif request_data['stock'].upper() in stocks_list:
                        for tag in tags_list:
                            get_tags_data(tag, result_data, stock=request_data['stock'].upper())
                    else:
                        msg_value = APIConstant.NOT_FOUND_ERROR.format(model="Stock")
                        result_data[msg_name] = msg_value
                
                elif ['tag'] == list(request_data.keys()):
                    if request_data['tag'] == "":
                        for tag in tags_list:
                            get_tags_data(tag, result_data)
                    elif request_data['tag'].upper() in tags_list:
                        get_tags_data(request_data['tag'].upper(), result_data)
                    else:
                        msg_value = APIConstant.TAG_VALUE_ERROR
                        result_data[msg_name] = msg_value

                else:
                    msg_value = APIConstant.INVALID_INPUT
                    result_data[msg_name] = msg_value
        
        except Exception as e:
            msg_value = APIConstant.COMMON_ERROR.format(e=e)
            result_data[msg_name] = msg_value
        
        finally:
            return jsonify(result_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)