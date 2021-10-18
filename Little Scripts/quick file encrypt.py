from datetime import datetime
from pathlib import Path

import shutil, os, pyAesCrypt, glob, time, getpass

def date():
    return str(datetime.now()).replace(":", "-")

def run(mode, one_time_passw):
    bufferSize = 64 * 1024

    if mode == "e":
        print("Running!")

        output_name = f"output-{date()}"

        Path("input").mkdir(exist_ok=True)
        Path(output_name).mkdir(exist_ok=True)

        run = True

        while 1:
            for file in glob.glob("input/*.*"):
                pyAesCrypt.encryptFile(file, file+".enc", one_time_passw, bufferSize)
                os.remove(file)

            for file in glob.glob("input/*.enc"):
                shutil.move(file, output_name)


            time.sleep(1)

    elif mode == "d":
        folder = input("Output~ ")

        run = True # datetime.now()
        bufferSize = 64 * 1024

        for file in glob.glob(f"{folder}/*.*"):
            pyAesCrypt.decryptFile(file, file.replace(".enc", ""), one_time_passw, bufferSize)
            os.remove(file)

while 1:
    o = getpass.getpass(prompt='Please enter your OPT~ ')

    print(f"Your password is {o}")

    c = input("Is this correct? [Y/N]~ ").lower()

    if c == "y":
        os.system("cls")
        break

    elif c == "n":
        pass

    else:
        print("Unknown Option!\nPlease try again.")

while 1:
    m = input("[E/D] ~ ").lower()
    run(m,o)
