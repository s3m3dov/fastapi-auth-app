import peewee
from .init_db import mysql_db


class User(peewee.Model):
    email = peewee.CharField(unique=True, index=True)
    hashed_password = peewee.CharField()
    is_active = peewee.BooleanField(default=True)
    is_superuser = peewee.BooleanField(default=False)
    fullname = peewee.CharField(null=True)

    class Meta:
        database = mysql_db


class Item(peewee.Model):
    title = peewee.CharField(index=True)
    description = peewee.CharField(index=True)
    owner = peewee.ForeignKeyField(User, backref="items")

    class Meta:
        database = mysql_db