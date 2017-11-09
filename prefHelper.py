from pathlib import Path

def loggedIn():
    my_file = Path(".auth/token")
    return my_file.is_file()
    
def deviceRegistered():
    my_file = Path(".auth/uuid")
    return my_file.is_file()
    
def deviceUUID():
    file = open('.auth/uuid','r')
    uuid = file.read()
    file.close()
    return uuid
    
def deviceToken():
    file = open('.auth/token','r')
    token = file.read()
    file.close()
    return token