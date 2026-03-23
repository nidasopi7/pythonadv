contact_info ={
    "Alice": "555-1234",
    "Bob": "555-5678"
}

print(contact_info["Alice"])

contact_info["Alice"] = "555-999"
print(contact_info)

contact_info["Ana"] = "123-234"
print(contact_info)

del contact_info["Bob"]
print(contact_info)

keys = contact_info.keys()
print(keys)

values = contact_info.values()
print(values)

print(contact_info.items())


contact_information = {
    "Alice": {
        "phone-number" : "554-234",
        "email": "alisa@gmail.com",
        "birthday": "20/11/2000"
    },
    "Bob": {
        "phone-number": "334-234",
        "email": "bob@gmail.com",
        "birthday": "20/12/2005"
    },
    "Eve": {
        "phone-number": "110-234",
        "email": "eve@gmail.com",
        "birthday": "04/08/2008"
    }
}

print(contact_information)

print(contact_information["Alice"])

grades = {
    ("John","Math"): 5,
   ("Alice","Biology"): 4,
    ("Bob","Physics"):2
}

john_math = grades[("John","Math")]
print(john_math)
print("John's grade in math is:",john_math)

grades[("Bob","Math")] = 3
print(grades)







