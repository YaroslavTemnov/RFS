def find_action (s):
    actions = "+-*/"
    cai = { } #cai - current action and index

    for i in s:
        if i in actions:
            cai.update({"action" : i})
            cai.update({"index" : s.find(i)})
    
    return cai

def converter(s):
    cai = find_action(s)
    triplets = {
        "ONE" : 1,
        "TWO" : 2,
        "THR" : 3,
        "FOU" : 4,
        "FIV" : 5,
        "SIX" : 6,
        "SEV" : 7,
        "EIG" : 8,
        "NIN" : 9,
        "ZER" : 0,
    }
    ct = " " #ct - current triple
    a = 0
    b = 0
    place = int(cai ["index"] / 3 - 1)
    for i in range (0, cai["index"], 3):
        ct = s[i : i + 3]
        a += triplets[ct] * (10 ** place)
        place -= 1
    place = int((len(s) - cai["index"] - 1) / 3 - 1)
    for i in range (cai["index"] + 1, len(s), 3):
        ct = s[i : i + 3]
        b += triplets[ct] * (10 ** place)
        place -= 1
    return a, b

def calculator(s):
    a, b = converter(s)
    cai = find_action(s)
    action = cai["action"]
    if action == "+":
        return int(a) + int(b)
    elif action == "-":
        return int(a) - int(b)
    elif action == "*":
        return int(a) * int(b)
    elif action == "/":
        return int(a) / int(b)
    
def converter_to_back(s):
    triplets = {
        1 : "ONE",
        2 : "TWO",
        3 : "THR",
        4 : "FOU",
        5 : "FIV",
        6 : "SIX",
        7 : "SEV",
        8 : "EIG",
        9 : "NIN",
        0 : "ZER"
    }
    n = str(calculator(s))
    rs = "" #rs - result string
    for i in n:
        rs += triplets[int(i)]
    return rs
        
        

s = input()

print(converter_to_back(s))