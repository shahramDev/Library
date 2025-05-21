from filelock import FileLock
import json
import os
from datetime import datetime
import bcrypt

class User:

    database = 'database/users.json'
    lockFile = database + '.lock'

    def __init__(self, userName, user = None):
        self.user = user
        self.userName = userName

    @classmethod
    def loadUsers(cls):
        if not os.path.exists(cls.database):
            with open(cls.database, 'w') as database:
                json.dump({}, database, indent=4)
        lock = FileLock(cls.lockFile)
        with lock:
            with open(cls.database,'r') as database:
                return json.load(database)
    
    @classmethod
    def getUser(cls,userName):
        users = cls.loadUsers()
        user = users.get(userName)
        return User(userName,user)
    
    def saveDatabase(self, users):
        lock = FileLock(self.lockFile)
        with lock:
            with open(self.database, 'w') as f:
                json.dump(users, f, indent=4)

    @classmethod
    def createUser(cls, userName, password):
        users = cls.loadUsers()
        if userName in users:
            return None
        user = User(userName)
        data = {
            "password": bcrypt.hashpw(password.encode(),bcrypt.gensalt()),
            "userId": 1000000 + len(users),
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
                    "manageAdmins": False,
                    "viewReports": False,
                    "userMessages": False,
                    "upgradeMemberships": False
                }
            },
            "addresses": {},
            "memberShip": {
                "level": "normal",
                "since": None,
                "to": None
            },
            "books": []
        }
        users[userName] = data
        user.saveDatabase(users)
        return user
    
    @property
    def password(self):
        return self.user["password"]

    @password.setter
    def password(self, value):
        self.user["password"] = bcrypt.hashpw(value.encode(),bcrypt.gensalt())

    @property
    def userId(self):
        return self.user["userId"]

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

    # Membership
    @property
    def membershipLevel(self):
        return self.user["memberShip"]["level"]

    @membershipLevel.setter
    def membershipLevel(self, value):
        self.user["memberShip"]["level"] = value

    @property
    def membershipSince(self):
        return self.user["memberShip"]["since"]

    @membershipSince.setter
    def membershipSince(self, value):
        self.user["memberShip"]["since"] = value

    @property
    def membershipTo(self):
        return self.user["memberShip"]["to"]

    @membershipTo.setter
    def membershipTo(self, value):
        self.user["memberShip"]["to"] = value

    # Books
    def addBook(self, bookId, status, fromDate, toDate=None, privacy=False):
        self.user["books"].append({
            "bookId": bookId,
            "status": status,
            "from": fromDate,
            "to": toDate,
            "privacy": privacy
        })

    def getBooks(self):
        return self.user["books"]