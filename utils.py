class DatabaseConfig:
    def __init__(self, host, port, schema, user, password):
        self.host = host
        self.port = port
        self.schema = schema
        self.user = user
        self.password = password


class RabbitConfig:
    def __init__(self, host):
        self.host = host
