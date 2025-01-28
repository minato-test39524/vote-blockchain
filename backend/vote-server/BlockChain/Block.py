from hashlib import sha256
import json

class Block:
    def __init__(
            self, 
            index, 
            timestamp, 
            previous_block_hash, # 前のブロックのハッシュ値
            data, # 投票データ
            hash=None
        ):
        self.index = index
        self.timestamp = timestamp
        self.previous_block_hash = previous_block_hash
        self.data = data
        self.block_hash = hash or self.calculate_hash()

    # ブロックのハッシュ値を計算
    def calculate_hash(self):
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'previous_block_hash': self.previous_block_hash,
            'data': self.data,
        }, sort_keys=True).encode()

        return sha256(block_string).hexdigest()