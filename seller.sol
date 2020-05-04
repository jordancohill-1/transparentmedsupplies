pragma solidity ^0.4.26;


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

