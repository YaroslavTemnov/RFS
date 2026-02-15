class Building:
    height = 10
    width = 20
    def __init__(self, name):
        self.name = name
class School(Building):
    students = 1000


sb1 = School(name="Some_building1")

print(sb1.height, sb1.students)