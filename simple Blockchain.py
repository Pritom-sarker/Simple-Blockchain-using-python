import hashlib
import json
import datetime
from flask import Flask,jsonify,request


# part 1-> Create Blockchain

class Blockchain:

    def __init__(self):
        self.chain=[]
        self.create_block(1,'0','Its 1st block')


    # create hash
    def hash_fun(self,st):
        return str(hashlib.sha256(str(st).encode()).hexdigest())

    # create block, No calculation inside this box, It use to append on chain
    def create_block(self,proof,prev_hash,dt):
        data = {
            'index': len(self.chain)+1,
            'time':str(datetime.datetime.now()),
            'proof': proof,
            'prev_hash':prev_hash,
            'data': dt
        }
        self.chain.append(data)


    # I need to value! for that value hash will start like "0000*************".
    # for this calculation I will use previous block proof valyue
    def proof_of_work(self,prev_prof):

        root = 0
        while True:
            hash_value = self.hash_fun(str(root**2-prev_prof**2))
            if str(hash_value)[:4]=="0000":
                break
            root+=1

        return root

    # chain is valid! if
    # 1. proof and previous block's proof creates a hash value that start with 4 zero
    # 2. hash and previous block hash same

    def chain_is_valid(self):

        for i in range(1,len(self.chain)):
            #1. Proof hash value

            hash_value = self.hash_fun(str(self.chain[i]['proof'] ** 2 - self.chain[i-1]['proof'] ** 2))
            if hash_value[:4] !="0000":
                print('proof issue')
                return False

            # 2.  make hash of the block

            prev_block_hash = self.hash_fun(str(json.dumps(self.chain[i-1])))

            if prev_block_hash != self.chain[i]['prev_hash']:
                print('Prev has issue')
                return False

        return True



# Part 2 - Mining our Blockchain

# Creating a Web App
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Creating a Blockchain
blockchain = Blockchain()

# Mining a new block
# To mine a new block we need 3 thing
# 1. Previous block hash
# 2. Proof value ( minor need to do calculation it takes time)
# 3. data that user want to add

@app.route('/mine_block', methods = ['GET'])
def mine_block():
    # 3. data that user want to add
    data = request.values.get('a')
    # 2. Proof value ( minor need to do calculation it takes time)
    proof = blockchain.proof_of_work(blockchain.chain[-1]['proof'])
    # 1. Previous block hash
    prev_hash = blockchain.hash_fun(str(json.dumps((blockchain.chain[-1]))))
    blockchain.create_block(proof,prev_hash,data)

    for block in blockchain.chain:
        print(block)
    print('--------------')
    return jsonify('DOne')

@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid    = blockchain.chain_is_valid()

    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'Pritom, we have a problem. The Blockchain is not valid.'}
    return jsonify(response), 200

# Running the app
app.run()
