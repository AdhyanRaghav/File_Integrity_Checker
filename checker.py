import json
import os
import hashlib
import subprocess
from pyexpat.errors import messages
from time import sleep

# BASE_DIR = "/home/adhyan/my_integrity_checker"
# BASELINE_FILE = os.path.join(BASE_DIR, "baseline.txt")
# SIGNATURE_FILE = os.path.join(BASE_DIR, "baseline.sig")
# TARGET_DIR = os.path.join(BASE_DIR, "target_files")

BASE_DIR = "/home/adhyan/my_integrity_checker"
BASELINE_FILE = os.path.join(BASE_DIR, "baseline.json")
SIGNATURE_FILE = os.path.join(BASE_DIR, "Signature.json")
TARGET_DIR = os.path.join(BASE_DIR, "target_files")

def hash_file(path):
    hash_obj = hashlib.sha256()

    with open(path, "rb") as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            hash_obj.update(chunk)

    return hash_obj.hexdigest()

def create_baseline():
    # with open(BASELINE_FILE, "w") as f1:
    #     for root, dirs, files in os.walk(TARGET_DIR):
    #         for file in files:
    #             path = os.path.join(root, file)
                # with open(path, "rb") as f:
                #     hash_obj = hashlib.sha256()
                #     while True:
                #         chunks = f.read(4096)
                #         if not chunks:
                #             break
                #         hash_obj.update(chunks)

                #f1.write(path + ": " + hash_file(path) + "\n")
    baseline_data={}

    for root,dic,files in os.walk(TARGET_DIR):
        for file in files:
            path=os.path.join(root,file)
            stat_info = os.stat(path)
            file_hash=hash_file(path)
            # file_mtime=os.path.getmtime(path)
            # file_size=os.path.getsize(path)
            # file_atime=os.path.getatime(path)
            baseline_data[path]={"hash": file_hash, "size": stat_info.st_size, "mtime": stat_info.st_mtime,"permissions":stat_info.st_mode,"uid":stat_info.st_uid,"gid":stat_info.st_gid,"inode":stat_info.st_ino}

    with open(BASELINE_FILE,"w") as f:
        json.dump(baseline_data,f)

    with open(SIGNATURE_FILE,"w") as f:
        #f1 .write(hash_file(BASELINE_FILE) + "\n")
        f.write(hash_file(BASELINE_FILE))

def send_notifications(title, message, file_path=None):
    subprocess.Popen(
        ["notify-send", title, message],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def check_integrity():
    hash_b1=hash_file(BASELINE_FILE)

    with open(SIGNATURE_FILE,"r") as file:
        content=file.read()

    if hash_b1==content:
        old_data = {}

        with open(BASELINE_FILE, "r") as f:
            # for line in f:
            #     line = line.strip()
            #     if not line:
            #         continue
            #     path, hash_val = line.split(": ", 1)
            #     old_data[path] = hash_val
            old_data=json.load(f)

        #print(old_data)

        new_data = {}

        for root, dic, file in os.walk(TARGET_DIR):
            for f1 in file:
                path = os.path.join(root, f1)
                file_hash=hash_file(path)
                stat_info=os.stat(path)
                new_data[path] = {"hash": file_hash,"size": stat_info.st_size, "mtime": stat_info.st_mtime,"permissions":stat_info.st_mode,"uid":stat_info.st_uid,"gid":stat_info.st_gid,"inode":stat_info.st_ino}

        #print(new_data)
        changes_detected = False
        for path in old_data:

            if path in new_data:
                if old_data[path]["hash"] != new_data[path]["hash"]:
                    message=f"File modified: {path}"
                    #print("File is modified!", path)
                    print(message)
                    send_notifications("Integrity Alert!",message,path)
                    changes_detected = True
                if old_data[path]["size"]!=new_data[path]["size"]:
                    message=f"File size changed: {path}"
                    #print("Size changed!",path)
                    print(message)
                    send_notifications("Integrity Alert!",message,path)
                    changes_detected=True
                if old_data[path]["mtime"]!=new_data[path]["mtime"]:
                    message=f"File modified: {path}"
                    print(message)
                    send_notifications("Integrity Alert!",message,path)
                    #print("File was modified!",path)
                    changes_detected=True
                if old_data[path]["permissions"]!=new_data[path]["permissions"]:
                    message=f"Permissions tampered!: {path}"
                    print(message)
                    send_notifications("Integrity Alert!",message,path)
                    #print("Permissions were changed!",path)
                    changes_detected=True
                if old_data[path]["uid"]!=new_data[path]["uid"]:
                    message=f"Uid tampered!: {path}"
                    print(message)
                    send_notifications("Integrity Alert!",message,path)
                    #print("Uid was changed!",path)
                    changes_detected=True
                if old_data[path]["gid"]!=new_data[path]["gid"]:
                    message=f"Group Id's tampered!"
                    print(message)
                    send_notifications("Integrity Alert!",message,path)
                    #print("Group id tampered!",path)
                    changes_detected=True
                if old_data[path]["inode"]!=new_data[path]["inode"]:
                    message=f"File Replaced!:{path}"
                    print(message)
                    send_notifications("Integrity Alert!",message,path)
                    #print("File was deleted and restored!",path)
                    changes_detected=True
            elif path not in new_data:
                #print("File is deleted", path)
                message = f"File Deleted!:{path}"
                print(message)
                send_notifications("Integrity Alert!",message,path)
                changes_detected = True

        for path in new_data:
            if path not in old_data:
                #print("New file created", path)
                message=f"New file detected: {path}"
                print(message)
                send_notifications("Integrity Alert!",message,path)
                changes_detected = True
        if not changes_detected:
            print("No changes detected")
            # message=f"No changed detected"
            # print(message)
            # send_notifications("Scan Complete", message)
    else:
        #print("Base file has been tampered!")
        message=f"Base file tampered!"
        print(message)
        send_notifications("Integrity Alert!",message,path)

# mode = input("Mode(init,check,monitor): ")
#
# if mode == "init":
#     create_baseline()
#
# elif mode == "check":
#     check_integrity()
#
# elif mode=="monitor":
#     import time
#     while True:
#         check_integrity()
#         time.sleep(10)
# else:
#     print("Invalid input")

if __name__=="__main__":
    import sys

    if len(sys.argv)>1 and sys.argv[1]=="init":
        create_baseline()

    while True:
        check_integrity()
        import time
        time.sleep(10)