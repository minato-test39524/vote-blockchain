from queue import Queue
from time import time
from BlockChain.Block import Block

class BlockChain():
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_votes = Queue()

    def create_genesis_block(self):
        genesis_block = Block(
            index=0,
            timestamp=time(),
            previous_block_hash='',
            data={
                'voter_id': None,
                'candidate_id': None,
                'timestamp': time(),
                'genesis_block': True
            }
        )
        return genesis_block.__dict__
    
    def get_latest_block(self):
        return self.chain[-1]
    
    def add_vote(self, voter_id, candidate_id):
        vote_data = {
            'voter_id': voter_id,
            'candidate_id': candidate_id,
            'timestamp': time(),
            'genesis_block': False
        }
        self.pending_votes.put(vote_data)

    def create_block(self, vote_data):
        if self.verify_vote(vote_data):
            block = Block(
                index=self.get_latest_block().get('index') + 1,
                timestamp=time(),
                previous_block_hash=self.get_latest_block().get('block_hash'),
                data=vote_data
            )
            self.chain.append(block.__dict__)
            return block.__dict__
        
        else:
            return "=== Failed to verify vote === \r\n" + "=== Failed to add block === \r\n" + "=== Voting data has been discarded ==="

    
    # vote_dataを検証
    def verify_vote(self, vote_data):
        checks = [
            self.is_first_vote(vote_data)

            # その他検証項目
        ]
        return all(checks)
    
    # 同じ有権者による投票が存在しないことを確認
    def is_first_vote(self, vote_data):
        voter_id = vote_data['voter_id']
        count_has_voted = 0
        for block in self.chain:
            if (block.get('data')['genesis_block'] == False and block.get('data')['voter_id'] == voter_id):
                count_has_voted += 1

        return count_has_voted == 0
    
    def get_total(self):
        totalDict = {}
        for block in self.chain:
            candidate_id = block.get('data')['candidate_id']

            if candidate_id is not None:    
                if candidate_id in totalDict.keys():
                    totalDict[candidate_id] += 1
                else:
                    totalDict.setdefault(candidate_id, 1)

        return totalDict
