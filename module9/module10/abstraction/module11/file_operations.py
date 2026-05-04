# Opening and closing the file
# file_path = "example.txt"
# file = open(file_path,"r")
#
# content = file.read()
# print(content)
#
# file.close()

import os

with open("example.txt", "r") as file:
    content = file.read()
    print(content)
    line = file.readline()
    print(line)
    lines = file.readlines()
    print(lines)

with open("example.txt", "w") as file:
    file.write("Pershendetje Orges!")

lines = ['Hello Wolrd\n', 'Welcome to Python\n']
with open("example.txt", "w") as file:
    file.writelines(lines)

#Moving the cursor
with open("example.txt", "r") as file:
    file.seek(0)
    data = file.read()
    print(data)

#Checking file existence
if os.path.exists('example.txt'):
    print("File exist")

#Reading and writing binary files
data = b'This is some binary data'
with open("example.bin",'wb') as file:
    file.write(data)

with open("example.bin",'rb') as binary_file:
    data= binary_file.read()
    print(data)


