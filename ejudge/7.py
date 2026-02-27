class reverse:
    def __init__(self, s):
        self.s = s
        self.index = len(s) 

    def __iter__(self):
        return self

    def __next__(self):
        if self.index <= 0:
            raise StopIteration
        
        self.index -= 1
        return self.s[self.index]
    
s = input()
result = reverse(s)
for i in range(len(s)):
    print(next(result), end ="")