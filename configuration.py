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


class FolderConfig:
    def __init__(self, src_folder, dst_folder):
        self.src_folder = src_folder
        self.dst_folder = dst_folder
