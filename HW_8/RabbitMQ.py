import pika

credentials = pika.PlainCredentials('nkqvpjmo', 'zg1W6Vcqr2KVZ7tKNYg8v7vtol0rDkCr')
connection = pika.BlockingConnection(pika.ConnectionParameters('sparrow-01.rmq.cloudamqp.com', 5672, 'nkqvpjmo', credentials))
channel = connection.channel()

channel.queue_declare(queue='hello_world')

if __name__ == '__main__':
    channel.basic_publish(exchange='', routing_key='hello_world', body='Hello world!'.encode())
    print(" [x] Sent 'Hello World!'")
    connection.close()
