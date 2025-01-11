from datetime import datetime
import requests
import re
import pika
from pymongo import MongoClient

client = MongoClient('mongodb://mongo:27017/')
db = client["database"]
collection = db["Jobs"]

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672))
channel = connection.channel()
channel.queue_declare(queue='job_queue', durable=True)


def getUserID(username):
    user_id = None
    url = f"https://www.facebook.com/{username}"

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7",
        "cache-control": "max-age=0",
        "cookie": "c_user=100000497696364; ps_n=1; ps_l=1; datr=o0nCZqLJH1T6JhRqKqpgPmRw; sb=Sl7GZpZokZcRgfA9WuC69Poe; b_user=61571256931160; fr=1RBlC8jc7ZAEu5QWi.AWWDpK5g0d0b-n39eez4gcAKCqA.Bnb_01..AAA.0.0.Bnb_01.AWWk7JzQTo8; xs=37%3A2WzrriQZZCXapg%3A2%3A1687268433%3A-1%3A15165%3AKeIOXNWM4jTpVg%3AAcUYLjAargmuxriAV1hF7OFbg6YP1lnDJULBFoXGcQpb; usida=eyJ2ZXIiOjEsImlkIjoiQXNwN2VxZDEyY29pa3kiLCJ0aW1lIjoxNzM1MzkyOTU1fQ%3D%3D; presence=C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1735394257740%2C%22v%22%3A1%7D; wd=719x953"    }

    response = requests.get(url, headers=headers)

    pattern = fr'"userVanity":"{re.escape(username)}","userID":"(\d+)"'
    match = re.search(pattern, response.text)
    if match:
        user_id = match.group(1)
        print(f"Found userID for {username}: {user_id}")
    else:
        print(f"No userID found for username: {username}")

    return user_id

def consume():
    def callback(ch, method, properties, body):
        print("consuming request")
        job_id, username = body.decode().split(",")
        user_id = getUserID(username)

        end_date = datetime.utcnow()
        status = "DONE"
        success = False
        error_message = None
        fbid = None

        if user_id:
            fbid = user_id
            success = True
        else:
            error_message = "User not found"

        collection.update_one(
            {"_id": job_id},
            {"$set": {
                "end_date": end_date,
                "status": status,
                "success": success,
                "error_message": error_message,
                "fbid": fbid
            }}
        )
    channel.basic_consume(queue='job_queue', on_message_callback=callback, auto_ack=True)
    print('Waiting for messages...')
    channel.start_consuming()

if __name__ == "__main__":
    import threading
    threading.Thread(target=consume, daemon=True).start()

    while True:
        continue