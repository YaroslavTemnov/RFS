def greet_everyone(greeting, *names):
    for name in names:
        print(greeting, name)

greeting = input()
greet_everyone(greeting,"name1", "name2", "name3" )