"""
File describes database with two tables
"""
from datetime import datetime
import peewee as pw

db = pw.SqliteDatabase('homegarage.db')


class BaseModel(pw.Model):
    """
    Class describes database table columns common for all tables
    """
    open_datetime = pw.DateTimeField(null=True, default=datetime.now())
    close_datetime = pw.DateTimeField(null=True)
    arrive_datetime = pw.DateTimeField(null=True)
    vin_code = pw.TextField(null=True)
    car_data = pw.TextField(null=True)
    kilometres = pw.TextField(null=True)
    works = pw.TextField(null=True)
    parts = pw.TextField(null=True)
    worker = pw.TextField(null=True)
    comment = pw.TextField(null=True)

    class Meta:
        database = db


class OpenedWorkOrders(BaseModel):
    """One of the database tables"""
    id = pw.AutoField()


class ClosedWorkOrders(OpenedWorkOrders):
    """One of the database tables"""
    id = pw.IntegerField(null=True)

    # pass
    class Meta:
        primary_key = pw.CompositeKey('id', 'close_datetime')


if __name__ == "__main__":
    pw.SqliteDatabase()
