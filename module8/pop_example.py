
class Rectangle:

    def __init__(self,length,width):
        self.length = length
        self.width = width

    def calculate_area(self):
            return self.length * self.width

    def calculate_perimeter(self):
            return 2 * (self.length * self.width)


my_rect = Rectangle( 2, 5)

area = my_rect.calculate_area()
perimeter = my_rect.calculate_perimeter()

print(f"Area: {area}")
print(f"Perimeter: {perimeter}")
