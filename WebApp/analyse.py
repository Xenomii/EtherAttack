import os
import subprocess


def analysecontract(filename):
    filename = filename.split('.')
    directory = "Contracts/" + filename[0]
    try:
        os.mkdir(directory)
    except OSError as error:
        print(error)
    subprocess.run(["./SlitherScanner.sh"])
    return 0
