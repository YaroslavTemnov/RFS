class Person:
    def __init__(self, name):
        self.name = name
        

class Student(Person):
    def __init__(self, name, gpa):
        super().__init__(name)
        self.gpa = gpa

    def display(self):
        print(F"Student: {self.name}, GPA: {self.gpa}")

n, g = [x for x in input().split()]

o = Student(name=n, gpa=g)
o.display()