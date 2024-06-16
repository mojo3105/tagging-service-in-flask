# Tagging Service using Flask
This is a Flask project that provides tagging services for stocks data. It utilizes Kafka for message queuing, Redis 
for caching & keeping tags information, and sqlite database for persisting stock information.

##  Setup Instructions
Follow the steps below to set up and run the Flask project.

### Prerequisites
Docker and Docker Compose
Python 3

### Set up Application
Use the provided docker-compose.yml file to create the Kafka and ZooKeeper containers.
```bash
    $ docker-compose up -d
```

You can see the following containers being created in your docker composed application. 
```bash
    1. zookeeper-flask (container with zookeeper instance)
    2. kafka-flask (container running kafka broker)
    3. redis-flask (container running redis server)
    4. tagging_service (container running flask application)
    5. kafka_producer (container to run kafka producer)
    6. kafka_consumer (container to run kafka consumer)
    7. kafka_redis_check (container to run scheduler script to flush redis)
```

Once docker application is running run the following commands to start producer and consumer.
First to run producer use following commands
```bash
    $ docker exec -it kafka_producer /bin/bash
    /app# python producer.py
```
Then to run consumer use following commands
```bash 
    $ docker exec -it kafka_consumer /bin/bash
    /app# python consumer.py
```
Once above setup is complete applicatio will be in running state.

## Access the Routes
```bash
/stocks/: This route allows performing CRUD operations on stock data.
/tags/: Use this route to retrieve tag data from Redis. It includes filters: tag or stock. The Json request will be like, 
    {
       "tag": "<tag_name>" or "stock": "<stock_name>"
    }
    to get all tags data can keep tags = "" and same for stock as well.
```

## Stop the Project
To stop the project use the following command
```bash
    $ docker-compose down
```

Conclusion
This Flask project provides tagging services for stocks data, utilizing Kafka for message queuing, Redis for 
caching, and a sqlite as a database to store data. By following the setup instructions and running the required 
scripts, you can perform CRUD operations on stock data and retrieve tag information based on a filter.
