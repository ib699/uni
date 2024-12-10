import pika
from dotenv import load_dotenv
import os
import service_2


class RabbitMQ:
    def __init__(self):
        load_dotenv()

        self.CLOUDAMQP_USER = os.getenv('CLOUDAMQP_USER')
        self.CLOUDAMQP_PASS = os.getenv('CLOUDAMQP_PASS')
        self.CLOUDAMQP_VH = os.getenv('CLOUDAMQP_VH')

        self.credentials = pika.PlainCredentials(self.CLOUDAMQP_USER, self.CLOUDAMQP_PASS)
        self.connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="cougar.rmq.cloudamqp.com", port=5672, virtual_host=self.CLOUDAMQP_VH,
                                      credentials=self.credentials, socket_timeout=2))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='songs')

    def push_message(self, song_id):
        self.channel.basic_publish(exchange='',
                              routing_key='songs',
                              body=song_id)

    def start_listening(self, handler):
        def callback(ch, method, properties, body):
            decoded_message = body.decode('utf-8')  # Decode the byte string to UTF-8 string
            print(f" [x] Received {decoded_message}")
            handler(decoded_message)  # Pass the decoded string to the handler
        self.channel.basic_consume(queue='songs', on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()
