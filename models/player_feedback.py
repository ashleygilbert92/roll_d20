from sqlalchemy import Column, Integer, ForeignKey, String, Date, Text
from sqlalchemy.orm import relationship

from . import Base
from . import CampaignModel


class PlayerFeedbackModel(Base):
    __tablename__ = 'player_feedback'

    id = Column(Integer, primary_key=True, autoincrement=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'), nullable=False)
    player_name = Column(String(64), nullable=False)
    date = Column(Date, nullable=False)
    feedback = Column(Text(65500), nullable=False)

    # Relationships
    campaign = relationship(CampaignModel, lazy=False, backref='player_feedback')

    def __repr__(self):
        return "<{}(id='{}', campaign_id='{}', play_name='{}')>".format(self.__class__.__name__,
                                                                        self.id,
                                                                        self.campaign_id,
                                                                        self.player_name)
