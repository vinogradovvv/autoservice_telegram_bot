"""
Database interface allows user to interact with database.
"""
from typing import Dict, List, Any, TypeVar
from peewee import ModelSelect, Model
from datetime import datetime
from database.model.model import BaseModel
from database.model.model import db

T = TypeVar("T")


def _store_data(db: db, model: T, *data: List[Dict]) -> None:
    """
    Function stores data in database table
    :param db: database
    :param model: table to store
    :param data: data to store
    :return: None
    """
    with db.atomic():
        model.insert_many(*data).execute()


def _retrieve_data(db: db, model: T, *columns: BaseModel) -> ModelSelect:
    """
    Function return select peewee object with any number of rows from database table
    :param db: database
    :param model: database table
    :param columns: table columns(if needed)
    :return: peewee select object
    """
    with db.atomic():
        response = model.select(*columns)

    return response


def _get_data(db: db, model: T, *columns: BaseModel) -> Model:
    """
    Function return select peewee object with one row from database table
    :param db: database
    :param model: database table
    :param columns: table columns(if needed)
    :return: peewee select object
    """
    with db.atomic():
        response = model.get(*columns)

    return response


def _update_data(db: db, model: T, id: int, colname: str, value: Any) -> None:
    """
    Function edits column value of row with given id in database table
    :param db: database
    :param model: database table
    :param id: id of row to edit
    :param colname: column name of value to edit
    :param value: value to edit
    :return: None
    """
    with db.atomic():
        row = model.get(model.id == id)
        setattr(row, colname, value)
        row.save()


def _delete_data(db: db, model: T, id: int) -> None:
    """
    Function delete row with given id from database table
    :param db: database
    :param model: table
    :param id: id of row
    :return: None
    """
    with db.atomic():
        row = model.get(model.id == id)
        row.delete_instance()


def _move_data(db: db, from_model: T, to_model: T, id: int) -> None:
    """
    Function takes a row with given id from one database table, write it to another table,
    and then delete it from first table
    :param db: database
    :param from_model: database table to delete row
    :param to_model: database table to write row
    :param id: id of row
    :return: None
    """
    with db.atomic():
        _update_data(db, from_model, id, 'close_datetime', datetime.now())
        row = from_model.select().where(from_model.id == id)
        row.close_datetime = datetime.now()
        to_model.insert_from(
            query=row,
            fields=to_model._meta.fields
        ).execute()
        row.get().delete_instance()


class DbInterface:
    """
    Database interface class with methodes to work with database
    """
    @staticmethod
    def create():
        """
        Methode to store data to the database table
        """
        return _store_data

    @staticmethod
    def retrieve():
        """
        Methode to retrieve data from the database table
        """
        return _retrieve_data

    @staticmethod
    def get():
        """
        Methode to get one line from the database table
        """
        return _get_data

    @staticmethod
    def update():
        """
        Methode to update data in the line of database table
        """
        return _update_data

    @staticmethod
    def remove():
        """
        Methode to delete line from the database table
        """
        return _delete_data

    @staticmethod
    def move():
        """
        Methode to move the line from one database table to another
        """
        return _move_data


if __name__ == "__main__":
    _store_data()
    _retrieve_data()
    _get_data()
    _update_data()
    _delete_data()
    _move_data()
    DbInterface()
