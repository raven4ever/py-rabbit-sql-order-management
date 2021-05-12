from configparser import RawConfigParser


class DatabaseConfig:
    def __init__(self, host, port, schema, user, password):
        self.host = host
        self.port = port
        self.schema = schema
        self.user = user
        self.password = password

    @classmethod
    def from_config_file(cls, config: RawConfigParser, section: str):
        host = config.get(section=section, option='host', raw=True)
        port = config.get(section=section, option='port', raw=True)
        schema = config.get(section=section, option='schema', raw=True)
        user = config.get(section=section, option='user', raw=True)
        password = config.get(section=section, option='password', raw=True)

        return cls(host, port, schema, user, password)


class RabbitConfig:
    def __init__(self, host, orders_q, response_q):
        self.host = host
        self.orders_q = orders_q
        self.response_q = response_q

    @classmethod
    def from_config_file(cls, config: RawConfigParser, section: str):
        host = config.get(section=section, option='host', raw=True)
        orders_q = config.get(section=section, option='send_orders_q', raw=True)
        response_q = config.get(section=section, option='send_results_q', raw=True)

        return cls(host, orders_q, response_q)


class FolderConfig:
    def __init__(self, src_folder, dst_folder):
        self.src_folder = src_folder
        self.dst_folder = dst_folder

    @classmethod
    def from_config_file(cls, config: RawConfigParser, section: str):
        src_folder = config.get(section=section, option='src_folder', raw=True)
        dst_folder = config.get(section=section, option='dst_folder', raw=True)

        return cls(src_folder, dst_folder)
