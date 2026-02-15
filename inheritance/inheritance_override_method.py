class Building:
    height = 10
    width = 20
    def __init__(self, name):
        self.name = name
    def info(self):
        return "name:", self.name, "height:", self.height,"width:", self.width

class School(Building):
    students = 1000
    def info(self):
        return "name:", self.name, "students:", self.students

sb1 = Building(name="Some Building")
sb0 = School(name="Some school named after someone")

print(sb1.info())
print(sb0.info())