from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from forms import BlockChainInput
from solcx import install_solc, compile_source, compile_files, link_code
from web3 import Web3
from web3.contract import ConciseContract
import json


app = Flask(__name__)
app.secret_key = "Blockchain Final"


contract_source_code = '''
pragma solidity ^0.6.4;

contract sellerContract{


	//init seller
	struct Seller{
		string name;
		uint quantity;
	}

	uint private supply;

	//declare seller obj
	Seller public seller_obj;
	Seller[] public sellers;

	//GET 
	function getSeller() public view returns (string memory, uint) { 
	    return (seller_obj.name, seller_obj.quantity);
	}

	//SET 
	function setSeller(string memory name, uint quantity) public {
	    seller_obj = Seller({name:name, quantity: quantity});
	    supply = supply + quantity;
	}

	//GET SUPPLY
	function getSupply() public returns (uint){
		return supply;
	}
    //REMOVE FROM SUPPLY
    function remove(string memory name, uint quantity) public {
	    seller_obj = Seller({name:name, quantity: quantity});
	    supply = supply - quantity;
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




@app.route("/", methods=['GET', 'POST'])
def index():
	tx_hash = contract_inst.functions.getSupply().transact()
	supply = contract_inst.functions.getSupply().call()
	return render_template('index.html', supply = supply)


@app.route('/add-data', methods=['GET', 'POST'])
def add_data():
	form = BlockChainInput()
	if request.method == 'GET':
		return render_template('add_data.html', form=form)
	else:
		message = 'Quantity must be an INTEGER'
		if form.validate_on_submit():
			company = request.form['company_name']
			quantity = request.form['quantity']
			quantity = int(quantity)


			tx_hash  = contract_inst.functions.setSeller(company, quantity).transact()
			addToBlockChain = contract_inst.functions.setSeller(company, quantity).call() 
			tx_hash = contract_inst.functions.getSupply().transact()
			supply = contract_inst.functions.getSupply().call()



			return redirect(url_for('index', supply=supply))
		return render_template('add_data.html', form=form, message=message)



@app.route('/remove-items', methods=['GET', 'POST'])
def remove_items():
	form = BlockChainInput()
	if request.method == 'GET':
		return render_template('remove_items.html', form=form)
	else:
		message = 'Quantity must be an INTEGER'
		if form.validate_on_submit():
			company = request.form['company_name']
			quantity = request.form['quantity']
			quantity = int(quantity)
			tx_hash = contract_inst.functions.getSupply().transact()
			supply = contract_inst.functions.getSupply().call()
			if supply == 0:
				message = 'No supply to remove'
				return render_template('remove_items.html', form=form, message=message)
			elif supply < quantity:
				message = 'There are only ' + str(supply) + ' items in the supply. Quantity must be less than the supply.'
				return render_template('remove_items.html', form=form, message=message)
			else:
				tx_hash  = contract_inst.functions.remove(company, quantity).transact()
				addToBlockChain = contract_inst.functions.remove(company, quantity).call() 
				tx_hash = contract_inst.functions.getSupply().transact()
				supply = contract_inst.functions.getSupply().call()
				return redirect(url_for('index', supply=supply))
		return render_template('remove_items.html', form=form, message=message)




@app.route("/about")
def about():
  return render_template("about.html")



if __name__ == "__main__":
  app.run(debug=True)
  