from sqlalchemy import Column, String, Integer
from flask_login import UserMixin
from werkzeug.security import check_password_hash

from . import Base


class UserModel(UserMixin, Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False)
    username = Column(String(32), unique=True, nullable=False)
    password = Column(String(256), nullable=False)

    def __init__(self, **kwargs):
        super(UserModel, self).__init__(**kwargs)

    # @property
    # def password(self):
    #     raise AttributeError('`password` is not a readable attribute')
    #
    # @password.setter
    # def password(self, password):
    #     self.password = generate_password_hash(password)
    #
    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "<{}(id='{}', name='{}', username='{}')>".format(self.__class__.__name__,
                                                                self.id,
                                                                self.name,
                                                                self.username)
