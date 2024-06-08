"""
Database core file
"""
from database.actions.db_actions import DbInterface
from database.model.model import db, OpenedWorkOrders, ClosedWorkOrders

db.connect()
db.create_tables([OpenedWorkOrders, ClosedWorkOrders])

db_actions = DbInterface()

if __name__ == "main":
    DbInterface()
