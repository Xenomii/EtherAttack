# 1. Introduction

Smart contracts are simply programs that run on the blockchain that help to automate the execution of a transaction. This helps all parties involved in the transaction to immediately identify the outcome without any intermediary involvement or time loss.

However, just like any piece of developed software, it can contain security vulnerabilities. This is where our tool steps in to analyse and identify these vulnerabilities and provide an alternative smart contract that exploits those identified vulnerabilities.

# 2. Environment Set-Up

First, you will need to pull the Github repository:

```
git pull https://github.com/Xenomii/EtherAttack
```

Then, you will need to setup the Python virtual environment:
```
cd EtherAttack
python -m venv .venv
```
Select the virtual environment that you just created:
```
.\venv\Scripts\activate
```
Install [Flask](https://flask.palletsprojects.com/en/2.0.x/installation/) dependencies:
```
pip install flask
```


# 3. Run Web Application
Once the setup is complete, you can now start up the web application to start using the tool:
```
cd WebApp
python app.py
```