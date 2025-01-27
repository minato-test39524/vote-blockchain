from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from typing import List

from databases.schemas import CandidateSchema, PostVoter, PostCandidate
from databases.models import VoterModel, CandidateModel
from databases.settings import SessionLocal

from BlockChain.BlockChain import BlockChain


bc = BlockChain()

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/voter")
def get_voter(
        db: Session = Depends(get_db)
    ):
    return db.query(VoterModel).all()

@app.get("/candidate", response_model=List[CandidateSchema])
def get_candidate(
        db: Session = Depends(get_db)    
    ):
    return db.query(CandidateModel).all()

@app.post("/voter")
def post_voter(
        voter: PostVoter,
        db: Session = Depends(get_db)
    ):
    db_model = VoterModel(voter_name = voter.voter_name)
    db.add(db_model)
    db.commit()

    return {"message": "success"}

@app.post("/candidate")
def post_candidate(
        candidate: PostCandidate,
        db: Session = Depends(get_db)
    ):
    db_model = CandidateModel(candidate_name = candidate.candidate_name)
    db.add(db_model)
    db.commit()

    return {"message": "success"}

@app.put("/voter/{id}")
def update_has_voted(
        id: int,
        db: Session = Depends(get_db)
    ):
    try:
        voter = db.query(VoterModel).filter(VoterModel.voter_id == id).first()

        voter.has_voted = False

        db.commit()

        return JSONResponse(content={"result": "success"})

    except SQLAlchemyError as e:

        db.rollback()
        raise HTTPException(status_code=500, detail=str(e)) from e
    
    finally:
        db.refresh(voter)


@app.delete("/voter/{id}")
def delete_voter(
        id: int,
        db: Session = Depends(get_db)
    ):
    delete_voter = db.query(VoterModel).filter(VoterModel.voter_id==id).one()
    db.delete(delete_voter)
    db.commit()

    return {"message": "success"}

@app.delete("/candidate/{id}")
def delete_candidate(
        id: int,
        db: Session = Depends(get_db)
    ):
    delete_candidate = db.query(CandidateModel).filter(CandidateModel.candidate_id==id).one()
    db.delete(delete_candidate)
    db.commit()

    return {"message": "success"}



# 以下ブロックチェーン関連API

@app.put("/vote/{voter_id}/{candidate_id}")
def vote_to_candidate(
        voter_id: int,
        candidate_id: int,
        db: Session = Depends(get_db),
        voter_model = VoterModel,
    ):

    voter_id_exists = db.query(db.query().exists().where(voter_model.voter_id == voter_id)).scalar()

    if voter_id_exists:
        has_voted = db.query(VoterModel).filter(VoterModel.voter_id == voter_id).one().has_voted
        if not has_voted:
            try:
                
                bc.add_vote(voter_id=voter_id, candidate_id=candidate_id)

                voter = db.query(VoterModel).filter(VoterModel.voter_id == voter_id).first()

                voter.has_voted = True

                db.commit()

                return JSONResponse(content={"vote_result": "success"})

            except SQLAlchemyError as e:

                db.rollback()
                raise HTTPException(status_code=500, detail=str(e)) from e
            
            finally:
                db.refresh(voter)
        else:
            return JSONResponse(content={"vote_result": "this voter has voted"})
    else:
        return JSONResponse(content={"vote_result": "vote id doesn't exist"})
    

@app.get("/blockchain/result")
def get_add_block_result():
    result = bc.create_block(bc.pending_votes.get())

    if isinstance(result, dict):
        return JSONResponse(content=result)
    else:
        return result

@app.get("/total")
def get_total():
    total_json = bc.get_total()
    return total_json

@app.get("/blockchain")
def get_blockchain_status():
    status = bc.chain
    return JSONResponse(content=status)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")