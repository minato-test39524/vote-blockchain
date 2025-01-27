from typing import List, Optional
from pydantic import BaseModel

class CandidateSchema(BaseModel):
    candidate_id: int
    candidate_name: str

class PostVoter(BaseModel):
    voter_name: str

class PostCandidate(BaseModel):
    candidate_name: str