import hashlib
import configparser

config = configparser.ConfigParser()
config.read("profiles/passwords.cfg")
print(config.sections())
password = "3047"


def passwordMatch(pswd, hash):
    pswd = hashlib.md5(pswd.encode())
    if pswd.hexdigest() == hash:
        return True
    return False


def generateHash(pswd):
    pswd = hashlib.md5(pswd.encode())
    return pswd.hexdigest()


# h = hashlib.md5(password.encode())
# print(generateHash('123'))
# print(passwordMatch(input(),h.hexdigest()))
