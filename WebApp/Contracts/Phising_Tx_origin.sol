// SPDX-License-Identifier: MIT
pragma solidity ^0.6.10;
contract Wallet {
    address public owner;

    constructor() public {
        owner = msg.sender;
    }
    function deposit() public payable {}
    function transfer(address payable _to, uint _amount) public {
        require(tx.origin == owner, "Not owner");

        (bool sent, ) = _to.call{value: _amount}("");
        require(sent, "Failed to send Ether");
    }
    function getBalance() public view returns(uint) {
        return address (this).balance;
    }
}
