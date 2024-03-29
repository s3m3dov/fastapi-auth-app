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


class IPData(peewee.Model):
    ip_address = peewee.CharField()
    ip_details = peewee.TextField()

    class Meta:
        database = mysql_db
