class Student:
    def __init__(self,name,age):
        self.__name = name
        self.__age = age

    def get_name(self):
        return self.__name

    def set_name(self,name):
        self.__name = name

    def get_age(self):
        return self.__age

    def set_age(self, age):
        self.__age = age

student1 = Student("Alice",20)

print(student1.get_name())
student1.set_name("Andi")
print(student1.get_name())

print(student1.get_age())