import os
print(os.curdir)
def isUser(name):
    if name.lower() != "readme.md":
        return True
    return False
print([i for i in os.listdir("./profiles/") if isUser(i)])