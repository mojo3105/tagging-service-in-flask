"""
The script contains kafka producer to generate values for stocks.
"""

#imports
from kafka import KafkaProducer
from app import app, Stocks
import json
import random
import time


try:
    # Create a Kafka producer instance
    producer = KafkaProducer(bootstrap_servers='kafka-flask:9092')
    # Send messages to the Kafka topic
    print(producer)
    topic = 'stocks_data'
    with app.app_context():
        while True:
            stocks = Stocks.query.all()
            serialized_data = list(map(lambda stock: stock.serialize_for_fluctuation(), stocks))
            for data in serialized_data:
                current_price = float(data['current_price'])
                price_range = current_price * 0.1

                # Generate a random price within the range
                random_price = random.uniform(current_price - price_range, current_price + price_range)

                # Update the stock price
                data['current_price'] = round(random_price, 2)
                # Send the updated stock data to the Kafka topic
                json_message = json.dumps(data)
                producer.send(topic, json_message.encode('utf-8'))
                print('sent', data)
            time.sleep(4)

except KeyboardInterrupt:
    # Close the producer connection
    producer.close()

except:
    raise