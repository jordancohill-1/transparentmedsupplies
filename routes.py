from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from solcx import compile_source, compile_files, link_code
from web3 import Web3
from web3.contract import ConciseContract
import json

app = Flask(__name__)

sellers = ['Company 1', 'Company 2']
values = [19898000, 95555440]
contract_source_code = '''
pragma solidity ^0.6.4;

contract sellerContract{


	//init seller
	struct seller{
		string name;
		uint quantity;
	}

	//declare seller obj
	seller public seller_obj;

	//GET 
	function getSeller() public view returns (string memory, uint) { 
	    return (seller_obj.name, seller_obj.quantity);
	}

	//SET 
	function setSeller(string memory name, uint quantity) public {
	    seller_obj = seller({name:name, quantity: quantity});
	}
}

'''

# Solidity Compiler
compiled_sol = compile_source(contract_source_code)
contract_interface = compiled_sol['<stdin>:sellerContract']


# web3.py instance
w3 = Web3(Web3.EthereumTesterProvider())
# set pre-funded account as sender
w3.eth.defaultAccount = w3.eth.accounts[0]

# Instantiate and deploy contract
ContractDeploy = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

# Submit the transaction that deploys the contract
tx_hash = ContractDeploy.constructor().transact()

# Wait for the transaction to be mined, and get the transaction receipt
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

# Create the contract instance with the newly-deployed address
contract_inst = w3.eth.contract(
    address=tx_receipt.contractAddress,
    abi=contract_interface['abi'],
)

data = [{"name": "Company1", "quantity": "93847338300"}, {"name": "Company2", "quantity": "89398834390"}]
 


@app.route("/", methods=['GET', 'POST'])
def index():

    return render_template('index.html', data=data)


@app.route("/about")
def about():
  return render_template("about.html")



if __name__ == "__main__":
  app.run(debug=True)
  