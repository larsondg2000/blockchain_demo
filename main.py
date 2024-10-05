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

col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])

with col1:
    st.image("bitcoin-btc-logo.png", caption=None, width=50)
with col2:
    st.image("ethereum-eth-logo.png", caption=None, width=50)
with col3:
    st.image("solana-sol-logo.png", caption=None, width=50)
with col4:
    st.image("xrp-xrp-logo.png", caption=None, width=50)
with col5:
    st.image("avalanche.png", caption=None, width=50)

rainbow_divider = """
<hr style="height:2px;border:none;background:linear-gradient(to right, red, orange, 
yellow, green, blue, indigo, violet);">
"""

st.markdown(rainbow_divider, unsafe_allow_html=True)

# Sidebar for adding transactions
st.sidebar.header("Create Transaction")
sender = st.sidebar.text_input("Sender")
recipient = st.sidebar.text_input("Recipient")
amount = st.sidebar.number_input("Amount", min_value=0.1, step=0.1)
if st.sidebar.button("Add Transaction"):
    if st.session_state.blockchain.new_transaction(sender, recipient, amount):
        st.sidebar.success("Transaction added to pending transactions!")
    else:
        st.sidebar.error("Pending transactions full. Mine a new block to add more.")

# Display pending transactions
st.subheader(":green[_Pending Transactions_]")
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
st.subheader(":green[Current Blockchain]")
for i, block in enumerate(st.session_state.blockchain.chain):
    if i == 0:
        st.subheader(":blue[_Genesis Block_]")
        st.write("_More info. on genesis block:_  https://en.bitcoin.it/wiki/Genesis_block")
    else:
        st.subheader(f"Block {i}")
    st.json(block)
    if i < len(st.session_state.blockchain.chain) - 1:
        st.markdown("⬇️")

# Add an interactive element to demonstrate hashing
# st.write("₿ ₿   ₿₿₿₿₿₿₿₿₿₿₿₿₿₿₿₿₿₿₿₿₿₿₿₿₿₿₿₿₿₿")
st.divider()
st.subheader(":green[See How Hashing Works]")
user_input = st.text_input("Enter some text to hash")
if user_input:
    hash_result = hashlib.sha256(user_input.encode()).hexdigest()
    st.write(f"SHA256 Hash: {hash_result}")
    st.info("Notice how even a small change in the input produces a completely different hash!")
st.image("sha.jpg", caption=None, width=None)

# Explain blockchain concepts
st.divider()
st.subheader(":green[How Blockchain Works]")

# Introduction
st.markdown("**Introduction**")
st.markdown("Blockchain technology is a decentralized and secure way of recording transactions. It’s most famously used in Bitcoin, a digital currency.")

# Key Components
st.markdown("**Key Components**")
st.markdown("""
- **Blocks:** Each block contains a list of transactions.
- **Chain:** Blocks are linked in a sequential chain.
- **Decentralized Network:** Multiple nodes (computers) validate transactions.
""")

# How Bitcoin Uses Blockchain
st.markdown("**How Bitcoin Uses Blockchain**")
st.markdown("""
- **Transaction Creation:** A Bitcoin transaction is initiated.
- **Transaction Verification:** Nodes in the network verify the transaction.
- **Block Creation:** Verified transactions are bundled into a new block.
- **Block Addition:** The new block is added to the blockchain.
""")

# Role of SHA-256
st.markdown("**Role of SHA-256**")
st.markdown("""
- **Hash Function:** SHA-256 is a cryptographic hash function used to ensure data integrity.
- **Block Hashing:** Each block includes a hash of the previous block, creating a secure link.
""")

# Example of SHA-256
st.markdown("**Example of SHA-256**")
st.markdown("""
- **Input:** The transaction data.
- **Process:** SHA-256 processes this data to produce a unique hash.
- **Output:** A fixed 256-bit hash that represents the transaction data.
""")

# Benefits of Blockchain
st.markdown("**Benefits of Blockchain**")
st.markdown("""
- **Security:** Cryptographic techniques like SHA-256 provide robust security.
- **Transparency:** Transactions are recorded on a public ledger.
- **Decentralization:** No single point of failure or control.
""")

# Links for more information
st.markdown("For more details on blockchain, visit [Wikipedia](https://en.wikipedia.org/wiki/Blockchain) and [Bitcoin](https://bitcoin.org/en/how-it-works).")
st.divider()
