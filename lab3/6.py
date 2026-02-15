class Shape:
    def area(self):
        return 0

    
class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = (int(length))
        self.width = int(width)
    def area(self):
        return self.length * self.width
    def __str__(self):
        return self.area()
    
a, b = [x for x in input().split()]

o = Rectangle(length = a, width = b)

print(o.area())