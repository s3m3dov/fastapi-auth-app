from typing import Any

import peewee
from pydantic.utils import GetterDict


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        result = getattr(self._obj, key, default)
        if isinstance(result, peewee.ModelSelect):
            return list(result)
        return result
