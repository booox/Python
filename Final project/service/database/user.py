from sqlalchemy import Column, Integer, String, Float
from connection import Base

class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(120), unique=True)
    user_id = Column(String(120), unique=True)
    name = Column(String(120))
    email = Column(String(120))
    mean_temperature = Column(Float)

    def __init__(self, username=None, user_id=None, name=None, \
        email=None, mean_temperature=None):

        self.username = username
        self.user_id = user_id
        self.email = email
        self.name = name
        self.mean_temperature = mean_temperature

    def __repr__(self):
        return '<User %r>' % (self.username)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'mean_temperature': self.mean_temperature
        }
