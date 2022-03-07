import fileinput
import os
import subprocess
import shutil
import re
import sys

OutputList = ["contract", "analysis", "dependency", "functionsummary", "summary"]
AttackDict = {
    "Version": "",
    "ContractName": "",
    "Deposit": "",
    "Withdraw": ""
}


# Analyse contract with Slither
def analyse(filename):
    filename = filename.split('.')
    directory = "Contracts/" + filename[0]
    try:
        os.mkdir(directory)
    except OSError as error:
        print(error)
    subprocess.run(["./SlitherScanner.sh"])
    moveFiles(filename)
    file = open(f"Contracts/{filename[0]}/analysis_{filename[0]}.txt")
    for line in file:
        if "https://github.com/crytic/slither/wiki/Detector-Documentation#reentrancy-vulnerabilities" in line:
            createReentrancyAttackContract(filename)
            break

    return


# Move all related outputs to a dedicated directory
def moveFiles(filename):
    for i in range(len(OutputList)):
        if i == 0:
            shutil.move(f"uploaded_files/temp_contract_file.sol",
                        f"Contracts/{filename[0]}/{OutputList[i]}_{filename[0]}.sol")
            continue
        shutil.move(f"TempStore/{OutputList[i]}.txt",
                    f"Contracts/{filename[0]}/{OutputList[i]}_{filename[0]}.txt")


def createReentrancyAttackContract(filename):
    temp = []
    file = open(f"Contracts/{filename[0]}/contract_{filename[0]}.sol")
    for line in file:
        if "pragma" in line:
            line.replace("\n","")
            AttackDict.update({"Version": line})
            continue
        if "contract" in line:
            x = line.split()
            AttackDict.update({"ContractName": x[1]})
            continue
        if "function" in line:
            x = line.split()
            y = x[1].split("(")
            temp.insert(0, y[0])
            continue
        if ("[msg.sender]" in line and "msg.value" in line) or "[msg.sender] += msg.value;" in line:
            AttackDict.update({"Deposit": temp[0]})
            continue
        if "msg.sender.call" in line:
            AttackDict.update({"Withdraw": temp[0]})
            continue
    print(AttackDict)

    # Copy attack template to contract directory
    shutil.copyfile("Attack/reentrancy_attack.sol", f"Contracts/{filename[0]}/attack_{filename[0]}.sol")

    # Modify attack contract
    replacement(filename, "*Version*", AttackDict["Version"])
    replacement(filename, "*ContractName*", AttackDict["ContractName"])
    replacement(filename, "*depositMethod*", AttackDict["Deposit"])
    replacement(filename, "*withdrawMethod*", AttackDict["Withdraw"])


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
