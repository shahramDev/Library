from filelock import FileLock
import json

class User:

    database = 'database/users.json'

    def __init__(self,userName):

        self.lock = FileLock(self.database + ".lock")
        self.load()
        self.userName = userName

    def load(self):
        with self.lock:
            with open(self.database,'r') as database:
                self.users = json.load(database)
    

    def getUser(self):
        userName = self.userName
        if userName in self.users.keys():
            self.user = self.users[userName]
        else:
            self.user = None
        return self

    def save(self):
        self.users[self.userName] = self.user
        with self.lock:
            with open(self.database, 'w') as database:
                json.dump(self.users, database, indent=4)