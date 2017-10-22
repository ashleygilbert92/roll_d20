from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from . import Base
from . import EncounterModel
from . import PlayerModel


class EncounterActionModel(Base):
    __tablename__ = 'encounter_actions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    encounter_id = Column(Integer, ForeignKey('encounters.id'), nullable=False)
    player_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    damage_taken = Column(Integer, default=0)
    damage_done = Column(Integer, default=0)
    spells_cast = Column(Integer, default=0)
    healing = Column(Integer, default=0)

    # Relationships
    encounter = relationship(EncounterModel, lazy=False, backref='encounter_action')
    player = relationship(PlayerModel, lazy=False, backref="encounter_action")

    def __repr__(self):
        return "<{}(id='{}', encounter_id='{}, player_id='{}')>".format(self.__class__.__name__,
                                                                        self.id,
                                                                        self.encounter_id,
                                                                        self.player_id)
