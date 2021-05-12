import configparser

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_entities import Base, Product
from utils import DatabaseConfig, RabbitConfig


def read_configuration(filename: str):
    configuration = configparser.RawConfigParser()
    configuration.read(filename)

    db = DatabaseConfig(configuration.get(section='database', option='host', raw=True),
                        configuration.get(section='database', option='port', raw=True),
                        configuration.get(section='database', option='schema', raw=True),
                        configuration.get(section='database', option='user', raw=True),
                        configuration.get(section='database', option='password', raw=True))

    rabbit = RabbitConfig(configuration.get(section='rabbitmq', option='host', raw=True))

    return db, rabbit


def create_db(db_config):
    eng = create_engine(
        f'mysql+pymysql://{db_config.user}:{db_config.password}@{db_config.host}:{db_config.port}/{db_config.schema}',
        echo=True)
    Session = sessionmaker(bind=eng)
    sess = Session(autocommit=True)

    return eng, sess


if __name__ == '__main__':
    db_config, rabbit_config = read_configuration('application.properties')

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

    all_prods = session.query(Product).all()
    print(all_prods)

    # Update from XML files
    # find all XML files in initial_xmls
