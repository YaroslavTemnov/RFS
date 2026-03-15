import os

files_in_ejudge = os.listdir("ejudge")
print("files in ejudge:")
for file in files_in_ejudge:
    if file.endswith(".py"):
        print(file)
