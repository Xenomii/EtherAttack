#!/bin/bash

slither --disable-color TempStore/temp_contract_file.sol &> TempStore/analysis.txt
slither --disable-color TempStore/temp_contract_file.sol --print data-dependency &> TempStore/dependency.txt
slither --disable-color TempStore/temp_contract_file.sol --print human-summary &> TempStore/summary.txt
slither --disable-color TempStore/temp_contract_file.sol --print function-summary &> TempStore/functionsummary.txt