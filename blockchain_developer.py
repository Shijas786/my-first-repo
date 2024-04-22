import hashlib
import json
from time import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []

        # Create the genesis block
        self.create_block(proof=1, previous_hash="0")

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }

        # Reset the list of pending transactions
        self.pending_transactions = []

        self.chain.append(block)
        return block

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def add_transaction(self, sender, receiver, amount):
        self.pending_transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })

    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f"{last_proof}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

# Initialize blockchain
blockchain = Blockchain()

# Add transactions
blockchain.add_transaction("Alice", "Bob", 10)
blockchain.add_transaction("Bob", "Charlie", 5)

# Mining
last_block = blockchain.chain[-1]
last_proof = last_block['proof']
proof = blockchain.proof_of_work(last_proof)

# Add new block to blockchain
blockchain.create_block(proof, blockchain.hash(last_block))

# Print blockchain
print("Blockchain:")
for block in blockchain.chain:
    print(block)
    print("-" * 50)

