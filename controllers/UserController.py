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
        user = User.getUser(userName)
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
        users = User.loadUsers()
        if userName in users:
            raise UsernameAlreadyExistsError('This user already exists.')
        cls.validateUserName(userName)
        cls.validatePassword(password)
        user = User(userName, None)
        user.createUser(userName,password)
        return cls(user)
    
    def setName(self,userInfo):
        if not len(userInfo) in [1,2] or not all(list(map(lambda text: re.fullmatch(r'\w{3,15}',text),userInfo))):
            raise InvalidNameOrLastNameError("name or last name has wrong syntax")
        name = userInfo[0]
        lastName = userInfo[1] if len(userInfo) == 2 else None
        self.user.name = name
        self.user.lastName = lastName
