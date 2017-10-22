from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship

from . import Base
from . import CampaignModel


class PlaySessionModel(Base):
    __tablename__ = 'play_sessions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'), nullable=False)
    date = Column(Date, nullable=False)
    description = Column(String(128), nullable=False)

    # Relationships
    campaign = relationship(CampaignModel, lazy=False, backref='play_session')

    def __repr__(self):
        return f"<{self.__class__.__name__}(id='{self.id}', campaign_id='{self.campaign_id}, date='{self.date}')>"
