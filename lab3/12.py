class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.base_salary = int(salary)

    def total_salary(self):
        return self.base_salary

class Manager(Employee):
    def __init__(self, name, salary, bonus_percent = None):
        super().__init__(name, salary)
        self.bonus_percent = int(bonus_percent)
    
    def total_salary(self):
        return self.base_salary * (1 + self.bonus_percent/100)
    
class Developer(Employee):
    def __init__(self, name, salary, completed_projects = None):
        super().__init__(name, salary)
        self.completed_projets = int(completed_projects)
    def total_salary(self):
        return self.base_salary + self.completed_projets * 500
    
class Intern(Employee):
    def __init__(self, name, salary):
        super().__init__(name, salary)
    def total_salary(self):
        return super().total_salary()
    
info = list(map(str, input().split()))
try:
    post, n, s, b = info
except:
    post, n, s, = info
    b = 0


emp1 = Developer(name=n, salary=s, completed_projects=b)
if post == "Employee":
    emp1 = Employee(name=n, salary=s)
elif post == "Manager":
    emp1 = Manager(name=n, salary=s, bonus_percent=b)
elif post == "Developer":
    emp1 = Developer(name=n, salary=s, completed_projects=b)
elif post == "Intern":
    emp1 = Intern(name=n, salary=s)
    

print(f"Name: {emp1.name}, Total: {emp1.total_salary():.2f}")