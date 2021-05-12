import pika
import sys

from configuration import RabbitConfig


def main(configuration: RabbitConfig, queue):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=configuration.host))
    channel = connection.channel()

    channel.queue_declare(queue=queue)

    def callback(ch, method, properties, body):
        print("   [x] Received %r" % body.decode())

    channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)

    print(f' [*] Waiting for messages on {queue}. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    config = RabbitConfig('localhost', 'ORDERS_RESULT', 'ORDERS_RESULT')

    try:
        main(config, 'ORDERS_RESULT')
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
