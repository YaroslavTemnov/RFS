class Shape:
    def area(self):
        return 0

class Square(Shape):
    length = int(input())
    def area(self):
        return self.length ** 2
    def __str__(self):
        return self.area()
    
o = Square()

print(o.area())