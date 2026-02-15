class Building:
    height = 10
    width = 20
    def __init__(self, name):
        self.name = name
    def info(self):
        return "name:", self.name, "height:", self.height,"width:", self.width

class School(Building):
    def __init__(self, name, opened):
        super().__init__(name)
        self.opened = opened
    students = 1000
    def info(self):
        return super().info(), self.students, self.opened
            

sb1 = Building(name="Some Building")
sb0 = School(name="Some school named after someone",opened=11111)

print(sb1.info())
print(sb0.info())