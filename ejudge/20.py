g = 0

def outer():
    n = 0
    
    def inner():
        nonlocal n
        global g
        
        for _ in range(m):
            scope, val = input().split()
            val = int(val)
            
            if scope == "global":
                g += val
            elif scope == "nonlocal":
                n += val
            elif scope == "local":
                x = 0
                x += val
    
    inner()
    
    print(g, n)

m = int(input())
outer()