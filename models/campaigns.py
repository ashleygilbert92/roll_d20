from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from . import Base
from . import UserModel


class CampaignModel(Base):
    __tablename__ = 'campaigns'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Relationships
    user = relationship(UserModel, lazy=False, backref='campaign')

    def __repr__(self):
        return "<{}(id='{}', name='{}', user_id='{}')>".format(self.__class__.__name__,
                                                               self.id,
                                                               self.name,
                                                               self.user_id)
