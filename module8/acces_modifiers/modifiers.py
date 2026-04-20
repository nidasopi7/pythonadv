class MyClass():
    def __init__(self):
        self.public_variable = "this is public"
        self.__private_variable = "this is private"
        self.__protected_variable = "this is protected variable"




my_class = MyClass()
print(my_class.public_variable)
#print(my_class.__public_variable)
print(my_class.protected_variable)