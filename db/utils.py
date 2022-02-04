from fastapi import Depends
from db.init_db import (
    mysql_db,
    db_state_default,
)


async def reset_db_state():
    mysql_db._state._state.set(db_state_default.copy())
    mysql_db._state.reset()


def get_db(db_state=Depends(reset_db_state)):
    try:
        mysql_db.connect()
        yield
    finally:
        if not mysql_db.is_closed():
            mysql_db.close()
