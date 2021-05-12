import configparser
import os
import shutil

import xmltodict as xmltodict
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from configuration import DatabaseConfig, RabbitConfig, FolderConfig
from db_entities import Base, Product


def read_configuration(filename: str):
    configuration = configparser.RawConfigParser()
    configuration.read(filename)

    db = DatabaseConfig.from_config_file(configuration, 'database')
    rabbit = RabbitConfig.from_config_file(configuration, 'rabbitmq')
    folder = FolderConfig.from_config_file(configuration, 'folder')

    return db, rabbit, folder


def create_db(config):
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


if __name__ == '__main__':
    db_config, rabbit_config, folder_config = read_configuration('application.properties')

    engine, session = create_db(db_config)

    # create the DB structure from entities
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    # insert few products
    session.add_all([
        Product(name='prod1', quantity=15),
        Product(name='prod2', quantity=3),
        Product(name='prod3', quantity=33),
        Product(name='prod4', quantity=47),
        Product(name='prod5', quantity=63)
    ])

    xml_files = get_xml_files(folder_config.src_folder)

    for file in xml_files:
        with open(file) as fd:
            doc = xmltodict.parse(fd.read())
        for product in doc['Stock']['Product']:
            session.query(Product) \
                .filter(Product.id == product['id']) \
                .update({Product.quantity: product['quantity']})

        # move to processes files
        shutil.move(file, file.replace(folder_config.src_folder, folder_config.dst_folder))

    all_prods = session.query(Product).all()
    print(all_prods)
