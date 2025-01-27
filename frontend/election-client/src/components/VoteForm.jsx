import axios from "axios";
import { useState } from "react";
import { Box, Button, FormControl, FormControlLabel, FormLabel, Radio, RadioGroup, TextField } from "@mui/material";
export const VoteForm = (props) => {
    const [ voterId, setVoterId] = useState(0);
    const [ candidate, setCandidate] = useState(null);
    const [ voteResult, setVoteResult ] = useState("");

    const { candidates } = props;

    const handleCandidateChange = (event) => {
        setCandidate((event.target).value);
    }

    const handleVoterIdChange = (event) => {
        setVoterId((event.target).value);
    }

    const handleCandidateReset = () => {
        setCandidate(null);
    }

    const handleVoterIdReset = () => {
        setVoterId(0);
    }

    const onClickVote = () => {
        axios.put(`http://localhost:8000/vote/${voterId}/${candidate}`)
        .then(res => {
            console.log(JSON.stringify(res.data));
            setVoteResult(JSON.stringify(res.data, null, 2));
            handleCandidateReset();
            handleVoterIdReset();
        })
        .catch(error => {
            console.log(error)
        });
    }

    return (
        <div style={{ border: "solid, lightsteelblue", borderRadius: "10px", height: "400px", width: "350px", backgroundColor: "aliceblue", padding: "8px", marginLeft: "16px"}} >
            <FormControl>
                <TextField
                    id="standard-number"
                    label="投票者ID"
                    type="number"
                    variant="standard"
                    slotProps={{
                        inputLabel: {
                            shrink: true,
                        },
                    }}
                    value={voterId}
                    onChange={handleVoterIdChange}
                    sx={{ marginBottom: "8px" }}
                />
                
                <FormLabel id="demo-radio-buttons-group-label">Candidates</FormLabel>
                <RadioGroup
                    aria-labelledby="demo-radio-buttons-group-label"
                    value={candidate}
                    onChange={handleCandidateChange}
                >
                    {candidates.map((candidate) => ( 
                        <FormControlLabel key={candidate.candidate_id} value={candidate.candidate_id} control={<Radio />} label={candidate.candidate_name}/>
                    ))}
                </RadioGroup>
                <Button variant="contained" onClick={onClickVote}>Vote</Button>
                
                vote result
                <Box component="section" sx={{ p: 2, border: '1px dashed grey' }}>  
                    {voteResult}
                </Box>
            </FormControl>

        </div>
    )
}