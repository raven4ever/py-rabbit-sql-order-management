import pika

from configuration import RabbitConfig


def get_rabbit_channel(configuration: RabbitConfig):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=configuration.host))
    channel = connection.channel()

    return channel


def send_orders_message(configuration: RabbitConfig, message):
    channel = get_rabbit_channel(configuration)
    channel.queue_declare(queue=configuration.orders_q)

    channel.basic_publish(exchange='', routing_key=configuration.orders_q, body=message)
    print(f'   [x] Sent message: {message} to {configuration.orders_q}')


def send_result_message(configuration: RabbitConfig, message):
    channel = get_rabbit_channel(configuration)

    channel.queue_declare(queue=configuration.response_q)

    channel.basic_publish(exchange='', routing_key=configuration.response_q, body=message)
    print(f'   [x] Sent message: {message} to {configuration.response_q}')


if __name__ == '__main__':
    config = RabbitConfig('localhost', 'ORDERS', 'ORDERS')
    msg = '{ "name":"John", "age":30, "city":"New York"}'
    valid = '{"client_name": "Name", "product_id": 3, "quantity": 15}'
    too_large = '{"client_name": "Name", "product_id": 3, "quantity": 1000}'

    send_orders_message(config, 'wazzzaaaaa!')
    send_orders_message(config, msg)
    send_orders_message(config, valid)
    send_orders_message(config, too_large)
