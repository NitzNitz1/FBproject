import pika
import json


RABBITMQ_HOST = "localhost"

def create_connection():
    return pika.BlockingConnection(pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        heartbeat=600,  # מונע ניתוקים אוטומטיים
        blocked_connection_timeout=300
    ))

connection = create_connection()
channel = connection.channel()
channel.queue_declare(queue='job_queue', durable=True)

def publish(job_id, username):
    message = json.dumps({"_id": job_id, "username": username})  # הפיכת המידע ל-JSON
    channel.basic_publish(
        exchange='', routing_key='job_queue', body=message,  # שליחת JSON אמיתי
        properties=pika.BasicProperties(delivery_mode=2)
    )
    print(f"📡 שולח הודעה ל-RabbitMQ: {message}")  # DEBUG


def consume(callback):
    channel.basic_consume(queue='job_queue', on_message_callback=callback, auto_ack=True)
    print("🐇 מאזין להודעות ב-RabbitMQ...")
    channel.start_consuming()
