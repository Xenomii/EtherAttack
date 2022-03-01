import subprocess


def analysecontract(filename):
    filename = filename.split('.')
    directory = "Contracts/" + filename[0]
    subprocess.run(["mkdir", directory])
    subprocess.run(["./SlitherScanner.sh"])
    return 0
