from sqlalchemy import  Boolean, Column, Integer, String
from databases.settings import Base

# 有権者モデル
class VoterModel(Base):
    __tablename__ = 'voter'

    voter_id = Column('voter_id', Integer, primary_key=True)
    voter_name = Column('voter_name', String(30))
    has_voted = Column('has_voted', Boolean, default=False)

# 候補者モデル
class CandidateModel(Base):
    __tablename__ = 'candidate'

    candidate_id = Column('candidate_id', Integer, primary_key=True)
    candidate_name = Column('candidate_name', String(30))