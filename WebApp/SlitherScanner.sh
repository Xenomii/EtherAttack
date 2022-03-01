#!/bin/bash

printf "==========================================================================================\n"
printf "\t\t\t\t\t\t\tSlither supports contacts written with solidity version >=0.4 <= 0.8.6\n"
printf "==========================================================================================\n\n"
slither --disable-color uploaded_files/temp_contract_file.sol &> Contracts/TempStore/contract.txt
slither --disable-color uploaded_files/temp_contract_file.sol --print data-dependency &> Contracts/TempStore/dependency.txt
slither --disable-color uploaded_files/temp_contract_file.sol --print human-summary &> Contracts/TempStore/summary.txt
slither --disable-color uploaded_files/temp_contract_file.sol --print evm &> Contracts/TempStore/evm.txt
slither --disable-color uploaded_files/temp_contract_file.sol --print function-summary &> Contracts/TempStore/functionsummary.txt
