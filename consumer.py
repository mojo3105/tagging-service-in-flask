"""
The script contains code for kafka consumer to consume latest stock price data an update tags
"""

#imports
from kafka import KafkaConsumer
import json
from app import app, db
from utils.tag_utils import *
from app import Stocks


try:
    # Create a Kafka consumer instance
    consumer = KafkaConsumer('stocks_data', bootstrap_servers='kafka-flask:9092')
    print(consumer)
    # Continuously poll for new messages
    with app.app_context():
        for message in consumer:
            json_message = message.value.decode('utf-8')

            # Parse the JSON string into a dictionary
            dict_message = json.loads(json_message)
            
            stock = Stocks.query.filter_by(stock_symbol=dict_message['stock']).first()
            stock = update_tags(stock, dict_message['current_price'])
            update_redis_values(stock)
            db.session.commit()
            print('received', dict_message)

except KeyboardInterrupt:
    # Close the consumer connection
    consumer.close()

except:
    raise