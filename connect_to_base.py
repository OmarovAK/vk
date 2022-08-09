import sqlalchemy


class DB_connections:
    def __init__(self, login, password, base):
        self.login = login
        self.password = password
        self.base = base

    def connect(self):
        db = f'postgresql://{self.login}:{self.password}@localhost:5432/{self.base}'
        engine = sqlalchemy.create_engine(db)
        connection = engine.connect()
        return connection


db = DB_connections('anuar', '123456', 'vk_bot')