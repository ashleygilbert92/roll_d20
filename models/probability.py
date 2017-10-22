from sqlalchemy import Column, Integer, Date

from . import Base


class ProbabilityModel(Base):
    __tablename__ = 'probability'

    id = Column(Integer, primary_key=True, autoincrement=True)
    roll = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)

    def __repr__(self):
        return "<{}(id='{}', roll='{}', date='{}')>".format(self.__class__.__name__,
                                                            self.id,
                                                            self.roll,
                                                            self.date)
