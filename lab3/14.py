n = int(input())
arr = [x for x in input().split()]
no = int(input())#no - number of operations


for i in range(0, no):
    operation = list(map(str, input().split()))
    if operation[0] == "add":
        arr = list(map(lambda x: int(x) + int(operation[1]), arr))
    elif operation[0] == "power":
        arr = list(map(lambda x: int(x) ** int(operation[1]), arr))
    elif operation[0] == "multiply":
        arr = list(map(lambda x: int(x) * int(operation[1]), arr))
    elif operation[0] == "abs":
        arr = list(map(lambda x: abs(int(x)), arr))
    operation.clear()
    
print(arr)