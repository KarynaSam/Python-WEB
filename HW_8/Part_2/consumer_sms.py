import pika
from mongoengine import connect, DoesNotExist
from models import Client


connect(host='mongodb+srv://Module9:wLcuUrRbu7CK2Y3d@eridas.p3ye6ga.mongodb.net/?retryWrites=true&w=majority')


def main():
    credentials = pika.PlainCredentials('nkqvpjmo', 'zg1W6Vcqr2KVZ7tKNYg8v7vtol0rDkCr')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('sparrow-01.rmq.cloudamqp.com', 5672, 'nkqvpjmo', credentials))
    channel = connection.channel()

    channel.queue_declare(queue='sms_queue')

    def callback(ch, method, body):
        try:
            message = body.decode()
            contact = Client.objects.get(id=message)
            print(f" [x] Recieved {message}")
            contact.sent_message = True
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except DoesNotExist:
            print(f'Can`t send message')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='sms_queue', on_message_callback=callback)
    print('Waiting for message')
    channel.start_consuming()


if __name__ == '__main__':
    main()