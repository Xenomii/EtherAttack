#!/bin/bash

printf "==========================================================================================\n"
printf "\t\t\t\t\t\t\tSlither supports contacts written with solidity version >=0.4 <= 0.8.6\n"
printf "==========================================================================================\n\n"
slither --disable-color uploaded_files/temp_contract_file.sol &> TempStore/analysis.txt
slither --disable-color uploaded_files/temp_contract_file.sol --print data-dependency &> TempStore/dependency.txt
slither --disable-color uploaded_files/temp_contract_file.sol --print human-summary &> TempStore/summary.txt
slither --disable-color uploaded_files/temp_contract_file.sol --print function-summary &> TempStore/functionsummary.txt
