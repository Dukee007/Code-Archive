import shutil, os, pyAesCrypt, glob, subprocess, ntpath

bufferSize = 64 * 1024

mode = input("E/D ~ ")
passw = input("PASSW (secure one pls :D) ~ ")
spassw = input("SECOND PASSW: (secure aswell) ~ ")

if mode.lower() == "e":
    target_folder = input("FOLDER (full path) ~ ")
    shutil.make_archive(os.path.basename(target_folder), 'zip', target_folder) # make the og zip

    pyAesCrypt.encryptFile(f"{os.path.basename(target_folder)}.zip", f"{os.path.basename(target_folder)}.zipenc", passw, bufferSize) # encrypt the og zip

    os.remove(f"{os.path.basename(target_folder)}.zip") # delete the og zip

    os.mkdir(f"{os.path.basename(target_folder)}-doubleencrypt") #make the second dir for the second zip

    shutil.move(f"{os.path.basename(target_folder)}.zipenc", f"{os.path.basename(target_folder)}-doubleencrypt")

    shutil.make_archive(f"{os.path.basename(target_folder)}-doubleencrypt", 'zip', f"{os.path.basename(target_folder)}-doubleencrypt") # make the second zip

    shutil.rmtree(f"{os.path.basename(target_folder)}-doubleencrypt")

    pyAesCrypt.encryptFile(f"{os.path.basename(target_folder)}-doubleencrypt.zip", f"{os.path.basename(target_folder)}.dea", spassw, bufferSize) # encrypt the og zip

    os.remove(f"{os.path.basename(target_folder)}-doubleencrypt.zip")

    print("done!")

elif mode.lower() == "d":
    target_file = input("FILE (full path) ~ ")

    pyAesCrypt.decryptFile(target_file, "decryptedp1.zip", spassw, bufferSize)

    shutil.unpack_archive("decryptedp1.zip", "decryptedp2")

    os.remove("decryptedp1.zip")

    folder_file = str(glob.glob("decryptedp2/*.zipenc")[0])
    file = ntpath.basename(str(glob.glob("decryptedp2/*.zipenc")[0]))

    shutil.move(folder_file, os.getcwd())

    pyAesCrypt.decryptFile(file, "decryptedp3.zip", passw, bufferSize)

    shutil.unpack_archive("decryptedp3.zip", "output")

    subprocess.Popen(r'explorer /select,"output"')

    os.remove(file)
    os.remove("decryptedp3.zip")
    shutil.rmtree("decryptedp2")

    print("done!")
