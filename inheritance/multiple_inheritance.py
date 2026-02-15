class Mammal:
    legs = 4
    child_eats = "milk"

class Cats(Mammal):
    speed = "fast"
    eats = "meat"

class domestic_cat(Cats):
    loves = ["owner", "to sleep", "to play", "to eat"]

c1 = domestic_cat()
c2 = Cats()
m1 = Mammal()
print(m1.legs, c1.legs, c1.speed,c1.loves, c2.eats, c2.child_eats)