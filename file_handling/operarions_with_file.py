import shutil
import os

file = open("sample.txt", "x")
file.close()
with open("sample.txt", "w") as f:
    f.write(f"filling my file with some text\n")
    f.close()

with open("sample.txt", "a") as f:
    f.write(f"adding some information by this method \n")
    f.close()

with open("sample.txt", "r") as f:
    for i in f:
        print(i)
    f.close()


with open("sample_copy.txt", "x"):
    shutil.copy("sample.txt", "sample_copy.txt")
    try:
        os.remove("sample.txt")
    except OSError:
        print("unsuccess")



with open("sample_copy.txt", "r") as f:
    print("Copy text:")
    lines = f.readlines()
    for line in lines:
        print(line.rstrip())