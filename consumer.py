import json
import pika
from datetime import datetime
from facebook_utils import get_user_id
from mongodb_utils import update_job

def process_message(ch, method, properties, body):
    try:
        data = json.loads(body)
        job_id = data["_id"]
        username = data["username"]

        update_job(job_id, {"status": "IN_PROGRESS"})

        user_id = get_user_id(username)
        end_time = datetime.utcnow()

        if user_id is not None:
            update_data = {
                "end_date": end_time,
                "status": "DONE",
                "success": True,
                "fbid": user_id,
                "error_message": None
            }
        else:
            update_data = {
                "end_date": end_time,
                "status": "DONE",
                "success": False,
                "fbid": None,
                "error_message": "User not found or inaccessible"
            }

        update_job(job_id, update_data)

    except Exception as e:
        print(" Error processing message:", e)

    ch.basic_ack(delivery_tag=method.delivery_tag)

def consume(callback):
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="job_queue", durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="job_queue", on_message_callback=callback)
    print("✅ Consumer is running and waiting for messages...")
    channel.start_consuming()

if __name__ == "__main__":
    consume(process_message)
