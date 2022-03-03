import os
import subprocess
import shutil

OutputList = ["contract", "dependency", "functionsummary", "summary"]


def analyse(filename):
    filename = filename.split('.')
    directory = "Contracts/" + filename[0]
    try:
        os.mkdir(directory)
    except OSError as error:
        print(error)
    subprocess.run(["./SlitherScanner.sh"])
    for i in range(len(OutputList)):
        shutil.move(f"Contracts/TempStore/{OutputList[i]}.txt",
                    f"Contracts/{filename[0]}/{OutputList[i]}_{filename[0]}.txt")
    return
