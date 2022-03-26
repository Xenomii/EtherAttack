import fileinput
import os
import subprocess
import shutil

OutputList = ["contract", "analysis", "dependency", "functionsummary", "summary"]
ReentrancyAttackDict = {
    "Version": "",
    "ContractName": "",
    "Deposit": "",
    "Withdraw": ""
}

TxOriginAttackDict = {
    "Version": "",
    "ContractName": "",
    "victim": "",
}


# ================================ ANALYSE MAIN FUNCTION =============================
# Analyse contract with Slither
def analyse(filename):
    filename = filename.split('.')
    directory = "Contracts/" + filename[0]
    try:
        os.mkdir(directory)
    except OSError as error:
        print(error)
    subprocess.run(["./SlitherScanner.sh"])
    move_files(filename)
    file = open(f"Contracts/{filename[0]}/analysis_{filename[0]}.txt")
    for line in file:
        if "https://github.com/crytic/slither/wiki/Detector-Documentation#reentrancy-vulnerabilities" in line:
            create_reentrancy_attack_contract(filename)
            break
        if "https://github.com/crytic/slither/wiki/Detector-Documentation#dangerous-usage-of-txorigin" in line:
            create_txorigin_attack_contract(filename)
            break
    return


# ================================ ATTACK CONTRACT CREATION FUNCTIONS =============================
def create_reentrancy_attack_contract(filename):
    temp = []
    file = open(f"Contracts/{filename[0]}/contract_{filename[0]}.sol")
    for line in file:
        if "pragma" in line:
            line.replace("\n", "")
            ReentrancyAttackDict.update({"Version": line})
            continue
        if "contract" in line:
            x = line.split()
            ReentrancyAttackDict.update({"ContractName": x[1]})
            continue
        if "function" in line:
            x = line.split()
            y = x[1].split("(")
            temp.insert(0, y[0])
            continue
        if ("[msg.sender]" in line and "msg.value" in line) or "[msg.sender] += msg.value;" in line:
            ReentrancyAttackDict.update({"Deposit": temp[0]})
            continue
        if "msg.sender.call" in line:
            ReentrancyAttackDict.update({"Withdraw": temp[0]})
            continue
    print(ReentrancyAttackDict)

    # Copy attack template to contract directory
    shutil.copyfile("Attack/reentrancy_attack.sol", f"Contracts/{filename[0]}/attack_{filename[0]}.sol")

    # Modify attack contract
    replacement(filename, "*Version*", ReentrancyAttackDict["Version"])
    replacement(filename, "*ContractName*", ReentrancyAttackDict["ContractName"])
    replacement(filename, "*depositMethod*", ReentrancyAttackDict["Deposit"])
    replacement(filename, "*withdrawMethod*", ReentrancyAttackDict["Withdraw"])


def create_txorigin_attack_contract(filename):
    file = open(f"Contracts/{filename[0]}/contract_{filename[0]}.sol")
    for line in file:
        if "pragma" in line:
            line.replace("\n", "")
            TxOriginAttackDict.update({"Version": line})
            continue
        if "contract" in line:
            x = line.split()
            TxOriginAttackDict.update({"ContractName": x[1]})
            continue
        if "address public" in line:
            x = line.split(" ")
            print("Got it")
            TxOriginAttackDict.update({"Victim": x[2]})
            continue
    print(TxOriginAttackDict)

    # Copy attack template to contract directory
    shutil.copyfile("Attack/Phising_Tx_origin_attack.sol", f"Contracts/{filename[0]}/attack_{filename[0]}.sol")

    # Modify attack contract
    replacement(filename, "*Version*", TxOriginAttackDict["Version"])
    replacement(filename, "*ContractName*", TxOriginAttackDict["ContractName"])
    replacement(filename, "*Victim*", TxOriginAttackDict["Victim"])


# ================================ UTILITY FUNCTIONS =============================
def replacement(filename, previousword, nextword):
    # opening the file in read mode
    file = open(f"Contracts/{filename[0]}/attack_{filename[0]}.sol", "r")
    content = ""
    # Replace attack template with variables from victim contract
    for line in file:
        line = line.strip()
        changes = line.replace(previousword, nextword)
        content = content + changes + "\n"

    file.close()
    # opening the file in write mode
    fileout = open(f"Contracts/{filename[0]}/attack_{filename[0]}.sol", "w")
    fileout.write(content)
    fileout.close()


# Move all related outputs to a dedicated directory
def move_files(filename):
    for i in range(len(OutputList)):
        if i == 0:
            shutil.move(f"TempStore/temp_contract_file.sol",
                        f"Contracts/{filename[0]}/{OutputList[i]}_{filename[0]}.sol")
            continue
        shutil.move(f"TempStore/{OutputList[i]}.txt",
                    f"Contracts/{filename[0]}/{OutputList[i]}_{filename[0]}.txt")

