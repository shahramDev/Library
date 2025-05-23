from models.User import User
from core.ErrorHandling import( 
    UserNotFoundError ,
    InvalidCredentialsError,
    UsernameAlreadyExistsError,
    InvalidPasswordError,
    InvalidUserNameError,
    InvalidNameOrLastNameError
)
import re
import bcrypt

class UserController:

    def __init__(self,user):
        self.user = user

    @classmethod
    def getUser(cls,userName):
        user = User.getUserByUsername(userName)
        if user is None:
            raise UserNotFoundError('User does not exist.')
        return cls(user)
    
    def checkPassword(self,password):
        if not bcrypt.checkpw(password.encode(),self.user.password.encode()):
            raise InvalidCredentialsError('password is wrong')
    
    @classmethod
    def signIn(cls,userName,password):
        userController = cls.getUser(userName)
        userController.checkPassword(password)
        return userController
    
    def validateUserName(userName):
        if not re.fullmatch(r'^\w{4,12}$', userName):
            raise InvalidUserNameError("❌ UserName must contain digits or letters and between 4 and 12 characters")
        
    def validatePassword(password):
        if not (8 <= len(password) <= 20):
            raise InvalidPasswordError("❌ Password must be between 8 and 20 characters.")
        if not re.search(r'[A-Za-z]', password):
            raise InvalidPasswordError("❌ Password must include at least one letter.")
        if not re.search(r'\d', password):
            raise InvalidPasswordError("❌ Password must include at least one digit.")      

    @classmethod
    def signUp(cls, userName, password):
        cls.validateUserName(userName)
        cls.validatePassword(password)
        user = User.createUser(userName,password)
        if user is None:
            raise UsernameAlreadyExistsError('This user already exists.')
        return cls(user)
    
    def setName(self,userInfo):
        if not len(userInfo) in [1,2] or not all(list(map(lambda text: re.fullmatch(r'\w{3,15}',text),userInfo))):
            raise InvalidNameOrLastNameError("name or last name has wrong syntax")
        name = userInfo[0]
        lastName = userInfo[1] if len(userInfo) == 2 else None
        self.user.name = name
        self.user.lastName = lastName
        self.user.updateUser()

    def getBooks(self):
        books = self.user.getBooks()
        return [
            {
                "bookId": book["bookId"],
                "status": book["status"],
                "from": book["from"],
                "to": book["to"],
                "privacy": book["privacy"]
            }
            for book in books
        ]
    
    def getProfile(self):
        return {
            "userName": self.user.userName,
            "name": self.user.name,
            "lastName": self.user.lastName,
            "email": self.user.email,
            "phoneNumber": self.user.phoneNumber,
            "age": self.user.age,
            "addresses": self.user.getAddresses(),
            "createdAt": self.user.createdAt,
            "isAdmin": self.user.isAdmin,
            "role": self.user.role,
            "addingBooks": self.user.getPermision("addingBooks"),
            "editingBooks": self.user.getPermision("editingBooks"),
            "removingBooks": self.user.getPermision("removingBooks"),
            "manageUsers": self.user.getPermision("manageUsers"),
            "manageAdmins": self.user.getPermision("manaageAdmins"),
            "viewReports": self.user.getPermision("viewReports"),
            "userMessages": self.user.getPermision("userMessages"),
        }

    def updateName(self, name):
        self.user.name = name
        self.user.updateUser()

    def updateLastName(self, lastName):
        self.user.lastName = lastName
        self.user.updateUser()

    def isValidEmail(self, email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
        if not re.match(pattern, email):
            raise Exception

    def updateEmail(self, email):
        self.user.email = email
        self.user.updateUser()

    def updatePhoneNumber(self, phone):
        self.user.phoneNumber = phone
        self.user.updateUser()

    def updateAge(self, age):
        try:
            self.user.age = int(age)
            self.user.updateUser()
        except ValueError:
            print("Invalid age.")

    def updateUserName(self, userName):
        self.validateUserName()
        users = User.loadUsers()
        if any(user["userName"] == userName for user in users.values()):
            raise UsernameAlreadyExistsError('This userName is already taken')
        self.user.userName = userName
        self.user.updateUser()

    def addAddress(self, label, country, city, address):
        self.user.addAddress(label, country, city, address)
        self.user.updateUser()
