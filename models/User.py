from filelock import FileLock
import json
import os
from datetime import datetime
import bcrypt

class User:

    database = 'database/users.json'
    lockFile = database + '.lock'

    def __init__(self, userId, user: dict = None ):
        self.user = user
        self.userId = userId

    @classmethod
    def loadUsers(cls):
        try:
            with open(cls.database,'r') as database:
                return json.load(database)
        except:
            return {}
    
    @classmethod
    def getUserById(cls, userId):
        users = cls.loadUsers()
        user = users.get(userId)
        return cls(userId, user) if user else None

    @classmethod
    def getUserByUsername(cls, username):
        users = cls.loadUsers()
        for uid, data in users.items():
            if data.get("userName") == username:
                return cls(uid, data)
        return None
    
    def saveDatabase(self, users: dict):
        with open(self.database, 'w') as database:
            json.dump(users, database, indent=4)

    def updateUser(self):
        lock = FileLock(self.lockFile)
        with lock:
            users = User.loadUsers()
            users.update({self.userId:self.user})
            self.saveDatabase(users)        

    @classmethod
    def createUser(cls, userName, password):
        lock = FileLock(cls.lockFile)
        with lock:
            users = cls.loadUsers()
            if any(user["userName"] == userName for user in users.values()):
                return None
            data = {
                "password": bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode(),
                "userName": userName,
                "name": None,
                "lastName": None,
                "email": None,
                "phoneNumber": None,
                "createdAt": datetime.now().isoformat(),
                "isActive": True,
                "deletedAt": None,
                "age": None,
                "userAccess": {
                    "isAdmin": False,
                    "role": "user",
                    "permissions": {
                        "addingBooks": False,
                        "editingBooks": False,
                        "removingBooks": False,
                        "manageUsers": False,
                        "manageAdmins": False
                    }
                },
                "addresses": {},
                "books": []
            }
            userId = str(1000000 + len(users))
            user = User(userId,data)
            users[userId] = data
            user.saveDatabase(users)
        return user
    
    @property
    def password(self):
        return self.user["password"]

    @password.setter
    def password(self, value):
        self.user["password"] = bcrypt.hashpw(value.encode(),bcrypt.gensalt()).decode()

    @property
    def userName(self):
        return self.user["userName"]
    
    @userName.setter
    def userName(self,value):
        self.user["userName"] = value

    @property
    def name(self):
        return self.user["name"]

    @name.setter
    def name(self, value):
        self.user["name"] = value

    @property
    def lastName(self):
        return self.user["lastName"]

    @lastName.setter
    def lastName(self, value):
        self.user["lastName"] = value

    @property
    def email(self):
        return self.user["email"]

    @email.setter
    def email(self, value):
        self.user["email"] = value

    @property
    def phoneNumber(self):
        return self.user["phoneNumber"]

    @phoneNumber.setter
    def phoneNumber(self, value):
        self.user["phoneNumber"] = value

    @property
    def createdAt(self):
        return self.user["createdAt"]

    @createdAt.setter
    def createdAt(self, value):
        self.user["createdAt"] = value

    @property
    def isActive(self):
        return self.user["isActive"]

    @isActive.setter
    def isActive(self, value):
        self.user["isActive"] = value

    @property
    def deletedAt(self):
        return self.user["deletedAt"]

    @deletedAt.setter
    def deletedAt(self, value):
        self.user["deletedAt"] = value

    @property
    def age(self):
        return self.user["age"]

    @age.setter
    def age(self, value):
        self.user["age"] = value

    # User Access
    @property
    def isAdmin(self):
        return self.user["userAccess"]["isAdmin"]

    @isAdmin.setter
    def isAdmin(self, value):
        self.user["userAccess"]["isAdmin"] = value

    @property
    def role(self):
        return self.user["userAccess"]["role"]

    @role.setter
    def role(self, value):
        self.user["userAccess"]["role"] = value

    def setPermission(self, permission, value):
        if permission in self.user["userAccess"]["permissions"]:
            self.user["userAccess"]["permissions"][permission] = value

    def getPermission(self, permission):
        return self.user["userAccess"]["permissions"].get(permission)

    # Addresses
    def addAddress(self, name, country, city, address):
        self.user["addresses"][name] = {"country": country, "city": city, "address": address}

    def getAddresses(self):
        return self.user["addresses"]
    
    def getAddress(self,name):
        return self.getAddresses()[name]

    # Books
    def addBook(self, bookId, status, fromDate, toDate=None, privacy=False):
        self.user["books"].append({
            "bookId": bookId,
            "status": status,
            "from": fromDate,
            "to": toDate,
            "privacy": privacy
        })
        self.updateUser()
    def getBooks(self):
        return self.user["books"]