import streamlit as st
import hashlib
import json
from time import time

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.new_block(previous_hash="The Times 03/Jan/2009 Chancellor on brink of second bailout for banks.", proof=100)

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.pending_transactions = []
        self.chain.append(block)
        return block

    @property
    def last_block(self):
        return self.chain[-1]

    def new_transaction(self, sender, recipient, amount):
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        if len(self.pending_transactions) < 3:
            self.pending_transactions.append(transaction)
            return len(self.pending_transactions)
        return False

    def hash(self, block):
        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object.encode()
        raw_hash = hashlib.sha256(block_string)
        hex_hash = raw_hash.hexdigest()
        return hex_hash

# Initialize session state
if 'blockchain' not in st.session_state:
    st.session_state.blockchain = Blockchain()

st.set_page_config(page_title="Blockchain Demo", page_icon=":material/currency_bitcoin:")

st.image("bc_demo.jpg", caption=None, width=None)

rainbow_divider = """
<hr style="height:2px;border:none;background:linear-gradient(to right, red, orange, 
yellow, green, blue, indigo, violet);">
"""

st.write("""
_**This interactive demo explains how a blockchain works. You can add transactions,
mine new blocks, and see how the blockchain maintains its integrity.**_
""")
# st.balloons()
st.markdown(rainbow_divider, unsafe_allow_html=True)

# Sidebar for adding transactions
st.sidebar.header("Add New Transaction")
sender = st.sidebar.text_input("Sender")
recipient = st.sidebar.text_input("Recipient")
amount = st.sidebar.number_input("Amount", min_value=0.1, step=0.1)
if st.sidebar.button("Add Transaction"):
    if st.session_state.blockchain.new_transaction(sender, recipient, amount):
        st.sidebar.success("Transaction added to pending transactions!")
    else:
        st.sidebar.error("Pending transactions full. Mine a new block to add more.")

# Display pending transactions
st.subheader(":blue[_Pending Transactions_]")
if st.session_state.blockchain.pending_transactions:
    for i, transaction in enumerate(st.session_state.blockchain.pending_transactions, 1):
        st.write(f"Transaction {i}:")
        st.json(transaction)
else:
    st.write("No pending transactions.")

# Mine new block
if st.button("Mine New Block"):
    if st.session_state.blockchain.pending_transactions:
        import random
        proof = random.randint(1000, 9999)
        st.session_state.blockchain.new_block(proof)
        st.success("New block mined and added to the blockchain!")
    else:
        st.error("No pending transactions to mine. Add some transactions first.")
st.divider()
# Display the blockchain
st.subheader(":blue[Current Blockchain]")
for i, block in enumerate(st.session_state.blockchain.chain):
    if i == 0:
        st.subheader(":green[_Genesis Block_]")
        st.write("_Read about the Bitcoin Genesis Block:_  https://en.bitcoin.it/wiki/Genesis_block")
    else:
        st.subheader(f"Block {i}")
    st.json(block)
    if i < len(st.session_state.blockchain.chain) - 1:
        st.markdown("⬇️")

# Explain blockchain concepts
st.divider()
st.subheader(":blue[How Blockchain Works]")
st.write("""
1. **Transactions**: Users create transactions (e.g., sending Bitcoin).
2. **Pending Transactions**: Transactions are added to a pending list (max 3 in this demo).
3. **Blocks**: Pending transactions are grouped into blocks when mined.
4. **Mining**: New blocks are added to the chain through a process called mining.
5. **Hashing**: Each block contains a unique hash and the hash of the previous block, creating a chain.
6. **Immutability**: Changing any information in a block would change its hash, breaking the chain.
""")

# Add an interactive element to demonstrate hashing
# st.write("₿ ₿ ₿  ₿₿₿₿₿₿₿₿₿₿₿₿₿₿₿₿₿₿₿₿₿₿₿₿₿₿₿₿₿₿₿₿₿₿")
st.divider()
st.subheader(":blue[See How Hashing Works]")
user_input = st.text_input("Enter some text to hash")
if user_input:
    hash_result = hashlib.sha256(user_input.encode()).hexdigest()
    st.write(f"SHA256 Hash: {hash_result}")
    st.info("Notice how even a small change in the input produces a completely different hash!")

st.image("sha.jpg", caption=None, width=None)