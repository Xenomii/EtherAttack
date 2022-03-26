# 1. Introduction

Smart contracts are simply programs that run on the blockchain that help to automate the execution of a transaction. This helps all parties involved in the transaction to immediately identify the outcome without any intermediary involvement or time loss.

However, just like any piece of developed software, it can contain security vulnerabilities. Since smart contracts are immutable by design, these vulnerabilities must be identified before they are deployed onto the blockchain network. Many tools have been developed to scan smart contract files and identify vulnerabilities so that developers can fix them before deployment.

Our tool aims to take it a step further by creating smart contracts that specifically exploit those identified vulnerabilities based on the uploaded smart contract file.

# 2. Target Platform
This project targets smart contracts built using the [Solidity](https://docs.soliditylang.org/en/v0.8.13/) language for the Ethereum blockchain.

# 2. Environment Set-Up
Currently, the project can only be executed on a Linux machine (preferrably Ubuntu 20.04.4 LTS). You will also need [Python](https://www.python.org/) installed on your machine.

Firstly, clone the project respository into a directory of your choice:
```
git clone https://github.com/Xenomii/EtherAttack
```
Next, install these Python tools onto your machine:
```
sudo apt install python3-pip python3-venv
```
Once that is complete, create a Python Virtual Environment in the project directory:
```
cd EtherAttack/WebApp
python3 -m venv .venv
```
Activate the Python Virtual Environment by inputting this command:
```
source .venv/bin/activate
```
You should be able to see a ``(.venv)`` that is appended at the start of the directory terminal output.

Next, install the dependencies required for this project usin ``pip``:
```
pip install -r requirements.txt
```
Since, this project aims to analyse smart contracts built using Solidity, the compiler will need to be installed:
```
solc-select install 0.6.10
```
Verify that the compiler has been installed:
```
solc-select versions
```
You should see the version number ``0.6.10`` in the terminal.

After verifying that the compiler has been installed properly, the version must be selected to be used globally:
```
solc-select use 0.6.10
```

# 4. Execute tool
After the environment set-up is complete, you can now run the tool. The tool uses the Python-Flask framework to render a web application that can be used to upload smart contract files and view the results.
```
cd EtherAttack/WebApp
python3 app.py
```

# 5. Testing
For this project, the [Remix IDE](https://docs.soliditylang.org/en/v0.8.13/) was used to test the generated attack smart contract against the uploaded smart contract.
