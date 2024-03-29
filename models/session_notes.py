from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from . import Base
from . import PlaySessionModel
from . import PlayerModel


class SessionNoteModel(Base):
    __tablename__ = 'session_notes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey('play_sessions.id'), nullable=False)
    notes = Column(Text(65500), nullable=False)

    # Relationships
    session = relationship(PlaySessionModel, lazy=False, backref='session_note')

    def __repr__(self):
        return "<{}(id='{}', session_id='{})>".format(self.__class__.__name__, self.id, self.session_id)
