



## abstract class and method overriding
from abc import ABC, abstractmethod



class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    # def area(self):
    #     return 3.14 * self.radius ** 2
    def perimier(self):
        return 3.14 * self.radius
        pass
    
class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height 

circle = Circle(5)
rectangle = Rectangle(4, 6) 

print(f"Area of the circle: {circle.area()}")
print(f"Area of the rectangle: {rectangle.area()}") 

            
    






