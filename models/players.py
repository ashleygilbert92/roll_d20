from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from . import Base
from . import CampaignModel


class PlayerModel(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True, autoincrement=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'), nullable=False)
    name = Column(String(32), nullable=False)
    class1 = Column(String(32), nullable=False)
    class2 = Column(String(32))
    level = Column(Integer, nullable=False)
    mythic_tier = Column(Integer)
    exp = Column(Integer, nullable=False)

    # Relationships
    campaign = relationship(CampaignModel, lazy=False, backref='player')

    def __repr__(self):
        return f"<{self.__class__.__name__}(id='{self.id}', campaign_id='{self.campaign_id}, name='{self.name}')>"
