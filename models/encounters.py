from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship

from . import Base
from . import PlaySessionModel


class EncounterModel(Base):
    __tablename__ = 'encounters'

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey('play_sessions.id'), nullable=False)
    name = Column(String(64), nullable=False)
    description = Column(String(128), nullable=False)

    # Relationships
    session = relationship(PlaySessionModel, lazy=False, backref='encounter')

    def __repr__(self):
        return "<{}(id='{}', session_id='{}, name='{}')>".format(self.__class__.__name__,
                                                                 self.id,
                                                                 self.session_id,
                                                                 self.name)
