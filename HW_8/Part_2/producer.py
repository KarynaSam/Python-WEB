import pika
from models import Client
from faker import Faker
from random import choice

fake = Faker('en_US')


def seed_clients(n):
    for _ in range(n):
        contact = Client(
            fullname=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
            address=fake.address(),
            best_method=choice(['SMS', 'Email'])
        )
        contact.save()
        print(f' {contact.fullname} added successfully')


def send_messages():
    credentials = pika.PlainCredentials('nkqvpjmo', 'zg1W6Vcqr2KVZ7tKNYg8v7vtol0rDkCr')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('sparrow-01.rmq.cloudamqp.com', 5672, 'nkqvpjmo', credentials))
    channel = connection.channel()
    channel.queue_declare(queue='email_queue')
    channel.queue_declare(queue='sms_queue')

    contacts = Client.objects()
    for contact in contacts:
        if contact.best_method == "SMS":
            channel.basic_publish(exchange='', routing_key='sms_queue', body=contact.id)
            print(f'[v] Send to {contact.fullname}')
        elif contact.best_method == "Email":
            channel.basic_publish(exchange='', routing_key='email_queue', body=contact.id)
            print(f'[v] Send to {contact.fullname}')

    connection.close()


if __name__ == '__main__':
    send_messages()