import configparser
import os
import shutil

import xmltodict as xmltodict
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from configuration import DatabaseConfig, RabbitConfig, FolderConfig
from db_entities import Base, Product


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
    Session = sessionmaker(bind=eng)
    sess = Session(autocommit=True)

    return eng, sess


def get_xml_files(xml_path: str):
    files = []
    for file in os.listdir(f'.{os.path.sep}{xml_path}'):
        if file.endswith('.xml'):
            files.append(os.path.join(f'.{os.path.sep}{xml_path}', file))

    return files


def insert_initial_data(sess):
    # insert few products
    sess.add_all([
        Product(name='prod1', quantity=15),
        Product(name='prod2', quantity=3),
        Product(name='prod3', quantity=33),
        Product(name='prod4', quantity=47),
        Product(name='prod5', quantity=63)
    ])


def process_xml_files(files, sess):
    for file in files:
        with open(file) as fd:
            doc = xmltodict.parse(fd.read())
        for product in doc['Stock']['Product']:
            sess.query(Product) \
                .filter(Product.id == product['id']) \
                .update({Product.quantity: product['quantity']})

        # move to processes files
        shutil.move(file, file.replace(folder_config.src_folder, folder_config.dst_folder))


if __name__ == '__main__':
    db_config, rabbit_config, folder_config = get_configuration('application.properties')

    engine, session = get_db_objects(db_config)

    # create the DB structure from entities
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    insert_initial_data(session)

    xml_files = get_xml_files(folder_config.src_folder)

    process_xml_files(xml_files, session)

    print(session.query(Product).all())
