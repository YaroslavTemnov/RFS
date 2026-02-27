import sys
import importlib

input = sys.stdin.read
data = input().split()

q = int(data[0])
index = 1

for _ in range(q):
    module_path = data[index]
    attr_name = data[index + 1]
    index += 2
    
    try:
        module = importlib.import_module(module_path)
        try:
            attr = getattr(module, attr_name)
            if callable(attr):
                print("CALLABLE")
            else:
                print("VALUE")
        except AttributeError:
            print("ATTRIBUTE_NOT_FOUND")
    except (ImportError, ModuleNotFoundError):
        print("MODULE_NOT_FOUND")