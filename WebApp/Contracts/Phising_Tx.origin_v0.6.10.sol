pragma solidity ^0.6.10;
contract Wallet {
    address public owner;
    constructor() public {
        owner = msg. sender;
    }
    function deposit() public payable (}
   function transfer(address payable to, uint amount) public {
        require(tx.origin == owner, "Not owner");
        (bool sent, ) = _to.call{value: amount}("");
        require(sent, "Failed to send Ether");
    function getBalance() public view returns(uint) {
        return address (this).balance;
    }
}
