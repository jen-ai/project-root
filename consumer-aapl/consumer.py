import pika
import json
from pymongo import MongoClient

# RabbitMQ Bağlantısı
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='MSFT')  # Kuyruk adı 'MSFT'

# MongoDB Bağlantısı
client = MongoClient('mongodb://mongodb-primary:27017/')
db = client['stockmarket']
collection = db['stocks']

def callback(ch, method, properties, body):
    data = json.loads(body)
    print(f"Received message: {data}")
    # Mesajdaki veriyi işleme
    avg_price = data['price']  # Örnekte doğrudan fiyatı alıyoruz
    collection.insert_one({'company': data['company'], 'average_price': avg_price})
    print(f"Data inserted into MongoDB: {data}")

# RabbitMQ'dan mesajları tüketme
channel.basic_consume(queue='MSFT', on_message_callback=callback, auto_ack=True)
print("Waiting for messages...")
channel.start_consuming()
