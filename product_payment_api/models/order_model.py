from sqlalchemy import func
from datetime import datetime

from psycopg2 import DataError, ProgrammingError

from db.database import db
from db.get_db_connection import get_cursor_data, get_connection_to_db


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.Integer)
    amount = db.Column(db.Float, nullable=False, default=0, server_default="0")
    creation_time = db.Column(db.DateTime(timezone=False), server_default=func.now())
    description = db.Column(db.String(10000))
    sign = db.Column(db.String(100))

    def __init__(self, id, currency, amount, sign, description='', creation_time=datetime.now()):
        self.id = id
        self.currency = currency
        self.amount = amount
        self.description = description
        self.sign = sign
        self.creation_time = creation_time

    @classmethod
    def create(cls, currency, amount, sign, description=''):
        """
        Creates an order, adds it to a DB and return created Order class obj.
        """
        query = f"""INSERT INTO {cls.__tablename__} (currency, amount, description, sign)
                    VALUES ('%(currency)s', '%(amount)s', '%(description)s', '%(sign)s')
                    RETURNING * ;"""
        try:
            id, currency, amount, creation_time, description, sign = get_cursor_data(
                query, {'currency': currency, 'amount': amount, 'description': description, 'sign': sign}
            )
            return Order(id=id, currency=currency, amount=amount, description=description, sign=sign)
        except(DataError, ProgrammingError):
            return None

    @classmethod
    def get_by_id(cls, id: int):
        """
        Returns an order with the specific id.
        """
        query = f"SELECT * FROM {cls.__tablename__} WHERE id = %(id)s"
        try:
            id, currency, amount, creation_time, description, sign = get_cursor_data(
                query, {'id': id}
            )
            return Order(id=id, currency=currency, amount=amount, description=description, sign=sign)
        except(DataError, ProgrammingError, TypeError):
            return None

    @classmethod
    def get_all(cls):
        """
        Returns ALL created orders.
        """
        query = f"SELECT * FROM {cls.__tablename__}"
        try:
            conn = get_connection_to_db()
            cur = conn.cursor()
            cur.execute(query)
            orders = cur.fetchall()
            all_users = [Order(id=id, currency=currency, amount=amount, sign=sign, description=description)
                         for id, currency, amount, creation_time, description, sign in orders]
            return all_users
        except(DataError, ProgrammingError, TypeError):
            return None

    @classmethod
    def delete_by_id(cls, id: int):
        """
        Deletes a specific order. Returns True id order was found and deleted from DB.
        """
        if not Order.get_by_id(id):
            return False
        query = f"DELETE FROM {cls.__tablename__} WHERE id = '%(id)s'"
        try:
            conn = get_connection_to_db()
            cur = conn.cursor()
            cur.execute(query % {'id': id})
            conn.commit()
            return True
        except(DataError, ProgrammingError):
            return False

    def to_dict(self):
        """
        Returns a dictionary with a stock data values.
        """
        return {
            'id': self.id,
            "currency": self.currency,
            "amount": self.amount,
            "creation_time": self.creation_time,
            "description": self.description,
            "sign": self.sign
        }
