class StringHandler:
    def getString(self):
        self.text = input()

    def printString(self):
        print(self.text.upper())
    

s = StringHandler()
s.getString()
s.printString()