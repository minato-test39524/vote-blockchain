import axios from 'axios';

import { useEffect, useState } from 'react';

import { VoteForm } from './components/VoteForm';
import { AddBlockForm } from './components/AddBlockForm';
import { ChainState } from './components/ChainState';
import { Total } from './components/Total';

function App() {
  // const [voterId, setVoterId] = useState()
  const [candidates, setCandidates] = useState([]);

  useEffect(() => {
    const getCandidates = async () => {
      const res = await axios.get(`http://localhost:8000/candidate`);
        
      let data = []
      for(let candidate of res.data) {
        data.push({candidate_id: candidate.candidate_id, candidate_name: candidate.candidate_name});
      }
      setCandidates(data);
    
    };
    getCandidates();
  }, []); //空の依存配列で、初回レンダリング時のみ実行



  return (
    <>
      <div style={{ display: "flex", textAlign: "left", whiteSpace: "nowrap" }}>
        <VoteForm candidates={candidates} />
        <AddBlockForm />
      </div>
      <div style={{ display: "flex", textAlign: "left", whiteSpace: "nowrap" }}>
        <Total />
        <ChainState />
      </div>
    </>
  );
}

export default App
