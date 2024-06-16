"""
The script contains code to delete old key-values of tags from redis.
"""

#imports
from datetime import date
import time
import schedule
import threading
from utils.tag_utils import create_redis_client


def delete_old_redis_keys():
    """
    The function will check and delete old redis key-values.
    """
    try:
        redis_client = create_redis_client()
        print(redis_client)
        while True:
            today_date = date.today().strftime("%d%m%Y")
            keys = redis_client.keys("*")
            print(today_date, keys)
            for key in keys:
                if key.decode('utf-8').split("_")[-1] != today_date:
                    redis_client.delete(key)
                    print(f"key {key} deleted")
            time.sleep(4)
    except:
        raise


if __name__ == "__main__":

    # Create a separate thread for the scheduler
    scheduler_thread = threading.Thread(target=lambda: schedule.every().day.at("15:30").do(delete_old_redis_keys))

    # Start the scheduler thread
    scheduler_thread.start()

    # Continuously run the scheduler
    while True:
        schedule.run_pending()
        time.sleep(1)