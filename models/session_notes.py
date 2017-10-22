from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from . import Base
from . import PlaySessionModel
from . import PlayerModel


class SessionNoteModel(Base):
    __tablename__ = 'session_notes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey('play_sessions.id'), nullable=False)
    player_id = Column(Integer, ForeignKey('players.id'))
    notes = Column(Text(65500), nullable=False)

    # Relationships
    session = relationship(PlaySessionModel, lazy=False, backref='session_note')
    player = relationship(PlayerModel, lazy=False, backref='session_note')

    def __repr__(self):
        return f"<{self.__class__.__name__}(id='{self.id}', session_id='{self.session_id}, " \
               f"player_id='{self.player_id}')>"
