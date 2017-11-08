from pathlib import Path

def loggedIn():
    my_file = Path(".auth/token")
    return my_file.is_file()