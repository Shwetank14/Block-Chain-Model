# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 14:56:53 2020

@author: shwet
"""

#importing the required libraries

import hashlib
import datetime
import json
from flask import Flask, jsonify

#part 1 - Buliding a blockChain

class Blockchain:
    
    def __init__(self):
        self.chain = []                                             # The chain represents the list_of_blocks
        self.create_block(proof = 1, prev_hash = '0')

    #Create block function 

    def create_block(self, proof, prev_hash):
        block = {'index' : len(self.chain)+1,                       # defining the properties or attributes of the block
                 'timeStamp' : str(datetime.datetime.now()),
                 'proof':proof,
                 'prev_hash':prev_hash
                 }
        self.chain.append(block)                        # Adding the block 
        return block
    
    def get_previous_Block(self):
        return self.chain[-1]
        
     #creating proof of work
     # principle - Hard to Find
     #           - Easy to Verify
    
    def proof_of_Work(self, prev_proof):
        new_proof = 1
        
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - prev_proof**2).encode()).hexdigest()         # the encode format converts the string in a right format that is expected by SHA256 function
            if hash_operation[:4] == '0000':
                check_proof == True
            else:
                new_proof += 1
                
            return new_proof
        
    #check if the blockchain is valid
    
    #this Function returns the cryptographic hash of the block
    def gethash(self, block):
        encoded_block = json.dumps(block, 
                    sort_keys = True).encode()
        
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self,chain):
        previous_block = chain[0]
        block_index = 1
        
        while block_index < len(chain):
            curr_block = chain[block_index]
            if curr_block['prev_hash'] != self.gethash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = curr_block['proof']
            hash_operation = hashlib.sha256(str(
                proof**2 - previous_proof**2
                ).encode()).hexdigest()
            
            if hash_operation[:4] != '0000':
                return False
            
            previous_block = curr_block
            block_index += 1
        
        return True
        
        
#part 2 - Mining our Blockchain

 # I -> Creating a Web App using Flask
 
app = Flask(__name__)
 
 
 
 
 # II -> Creating a BlockChain using the class defined above

blockchain = Blockchain()



 # Mine a new Block
 
@app.route('/mine_block',methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_Block()
    previous_proof = previous_block['proof']
    
    proof = blockchain.proof_of_Work(previous_proof)
    
    previous_hash = blockchain.gethash(previous_block)
    
    block = blockchain.create_block(proof, previous_hash)
    
    response = {'messgae':'Congrats your block is mined.',
                'index':block['index'],
                'timestamp':block['timeStamp'],
                'proof':block['proof'],
                'previous_hash':block['prev_hash']}
    
    return jsonify(response),200        #200 HTTP status scope 200 -> OK
    
     
 #displaying full blockchain in postman
 
@app.route('/get_chain',methods = ['GET'])

def get_chain():
    response = {'chain':blockchain.chain,
                'length':len(blockchain.chain)}

    return jsonify(response),200


# Validity check of the Block

@app.route('/is_valid',methods = ['GET'])

def is_valid():
    
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    
    if is_valid:
        response = {'Message':'Everything seems to be fine with the blockchain.'}
    else:
        response = {'Message':'OOPS! the blockchain is not valid!!'}
    
    return jsonify(response),200


# Running The app
app.run(host='0.0.0.0',port= 5000)











