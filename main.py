import configparser
import json
import os
import shutil
from json import JSONDecodeError

import pika
import xmltodict as xmltodict
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import rabbit_sender
from configuration import DatabaseConfig, RabbitConfig, FolderConfig
from db_entities import Base, Product, Order, OrderStatus


def get_configuration(filename: str):
    configuration = configparser.RawConfigParser()
    configuration.read(filename)

    db = DatabaseConfig.from_config_file(configuration, 'database')
    rabbit = RabbitConfig.from_config_file(configuration, 'rabbitmq')
    folder = FolderConfig.from_config_file(configuration, 'folder')

    return db, rabbit, folder


def get_db_objects(config):
    eng = create_engine(
        f'mysql+pymysql://{config.user}:{config.password}@{config.host}:{config.port}/{config.schema}',
        echo=True)

    return eng


def get_xml_files(xml_path: str):
    files = []
    for file in os.listdir(f'.{os.path.sep}{xml_path}'):
        if file.endswith('.xml'):
            files.append(os.path.join(f'.{os.path.sep}{xml_path}', file))

    return files


def insert_initial_data(engine):
    Session = sessionmaker(bind=engine)
    sess = Session()

    # insert few products
    sess.add_all([
        Product(name='prod1', quantity=15),
        Product(name='prod2', quantity=3),
        Product(name='prod3', quantity=33),
        Product(name='prod4', quantity=47),
        Product(name='prod5', quantity=63)
    ])
    sess.commit()


def process_xml_files(files, engine):
    Session = sessionmaker(bind=engine)
    sess = Session()

    for file in files:
        with open(file) as fd:
            doc = xmltodict.parse(fd.read())
        for product in doc['Stock']['Product']:
            sess.query(Product) \
                .filter(Product.id == product['id']) \
                .update({Product.quantity: product['quantity']})

        # move to processes files
        shutil.move(file, file.replace(folder_config.src_folder, folder_config.dst_folder))
    sess.commit()


if __name__ == '__main__':
    db_config, rabbit_config, folder_config = get_configuration('application.properties')

    engine = get_db_objects(db_config)

    # create the DB structure from entities
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    insert_initial_data(engine)

    xml_files = get_xml_files(folder_config.src_folder)

    process_xml_files(xml_files, engine)


    def callback(ch, method, properties, body):
        Session = sessionmaker(bind=engine)
        sess = Session()

        try:
            raw_order = json.loads(body.decode())
            q = raw_order['quantity']
            product = sess.query(Product).get(raw_order['product_id'])

            print(product)

            if product is not None and product.quantity >= q:
                order = Order(client_name=raw_order['client_name'],
                              status=OrderStatus.ACCEPTED,
                              product=product)
            else:
                order = Order(client_name=raw_order['client_name'],
                              status=OrderStatus.INSUFFICIENT_STOCK,
                              product=product)

            product.quantity = product.quantity - q
            sess.add(order)
            sess.commit()

            response = {
                "order_id": order.id,
                "order_status": order.status
            }

            rabbit_sender.send_result_message(rabbit_config, str(response))
        except JSONDecodeError:
            print('Please send a JSON message!!!')
        except KeyError:
            print('Please send a valid JSON schema!!!')


    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_config.host))
    channel = connection.channel()
    channel.queue_declare(queue=rabbit_config.orders_q)
    channel.basic_consume(queue=rabbit_config.orders_q, on_message_callback=callback, auto_ack=True)
    print(f' [*] Waiting for messages on {rabbit_config.orders_q}. To exit press CTRL+C')
    channel.start_consuming()
