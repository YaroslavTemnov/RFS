class Family:
    lastname = "Pupa"
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def info(self):
        return self.name, self.lastname, self.age


person1 = Family(name="Aza", age=20)
print(person1.info())
Family.lastname = "Lupa"
print(person1.info())