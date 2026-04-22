from module9.animal import animal


class Dog(Animal):

    def sound(self):
        print("WOOF! WOOF!")

    def description(self):
        super().description()
        print(f"Breed:{self.breed}")


animal = Animal("Generic Animal")
animal.sound()
animal.description()

dog = Dog( name:"Rex", breed:"Gold Retriever")
dog.sound()
dog.description()

