from environs import Env
from contextvars import ContextVar

import peewee

# Environment
env = Env()
env.read_env()

DATABASE_NAME = env("MYSQL_DATABASE", default="mysql_db")
DATABASE_USER = env("MYSQL_USER", default="mysql")
DATABASE_PASS = env("MYSQL_PASSWORD", default="mysql")
DATABASE_PORT = env("MYSQL_HOST", default="db")
DATABASE_PORT = env.int("MYSQL_PORT", default=3306)


db_state_default = {"closed": None, "conn": None, "ctx": None, "transactions": None}
db_state = ContextVar("db_state", default=db_state_default.copy())


class PeeweeConnectionState(peewee._ConnectionState):
    def __init__(self, **kwargs):
        super().__setattr__("_state", db_state)
        super().__init__(**kwargs)

    def __setattr__(self, name, value):
        self._state.get()[name] = value

    def __getattr__(self, name):
        return self._state.get()[name]


db = peewee.MySQLDatabase(DATABASE_NAME, user=DATABASE_USER, password=DATABASE_PASS, host="db", port=DATABASE_PORT)

db._state = PeeweeConnectionState()

# Peewee was not designed for async frameworks, or with them in mind.
