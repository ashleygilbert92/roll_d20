from sqlalchemy import Column, String, Integer

from . import Base


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False)
    username = Column(String(32), unique=True, nullable=False)
    password = Column(String(64), nullable=False)

    def __repr__(self):
        return f"<{self.__class__.__name__}(id='{self.id}', name='{self.name}', username='{self.username}')>"
