class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = 20
    def __str__(self):
        print(f"{self.name}:{self.age}")


p1 = Person(name="Name", age="20")
p1.__str__()
