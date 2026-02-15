class Circle:
    pi = 3.14159
    def __init__(self, radius):
        self.radius = int(radius)
    def area(self): 
        self.result = self.radius**2 * self.pi
        return(f"{self.result:.2f}")



o = Circle(radius=input())
print(o.area())