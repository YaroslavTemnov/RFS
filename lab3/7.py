from math import sqrt


class Point:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
    def show(self):
        return self.x, self.y
    def move(self, new_x, new_y):
        self.new_x = int(new_x)
        self.new_y = int(new_y)
        return self.new_x, self.new_y
    def dist(self, other_point):
        self.dx = int(other_point[0])
        self.dy = int(other_point[1])
        self.distance = sqrt((self.dx - self.new_x)**2 + (self.dy - self.new_y)**2)
        return(f"{self.distance:.2f}")

a, b = [x for x in input().split()]
a_new, b_new = [x for x in input().split()]
other_point = [x for x in input().split()]
o = Point(x=a, y=b)

print(o.show())
print(o.move(a_new, b_new))
print(o.dist(other_point))
