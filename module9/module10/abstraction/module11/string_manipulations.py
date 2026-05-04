with open("example.txt", "r") as file:
    for line in file:
        cleaned_line = line.strip().split()
        print(cleaned_line)


name = "Alice"
age = 20

with open("output.txt","w") as file:
    file.write("Name:" + name + "\n")
    file.write("Age:" + str(age) + "\n")