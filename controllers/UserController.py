from models.User import User
from core.ErrorHandling import UserNotFoundError ,InvalidCredentialsError,UsernameAlreadyExistsError ,InvalidPasswordError ,InvalidUserNameError

import re

class UserController:
    def getUser(self,userName):
        userData = User(userName).getUser().user
        if userData is None:
            raise UserNotFoundError('User does not exist.')
        self.user = userData
        return self
    def checkUser(self,password):
        if self.user["password"] != password:
            raise InvalidCredentialsError('password is wrong')
        return True
    def signUp(self,userName,password):
        userData = User(userName)
        if userData.getUser().user is not None:
            raise UsernameAlreadyExistsError('this user already exists')
        if self.validate(userName,password):
            userData.user = dict()
            userData.user["password"] = password
            userData.user["userAccess"] = dict()
            userData.user["userAccess"]["isAdmin"] = False
            userData.signUp()
            return userData
    def validate(self, userName, password):
        self.validateUserName(userName)
        self.validatePassword(password)
        return True
    def validateUserName(self, userName):
        if not re.fullmatch(r'^\w{4,12}$', userName):
            raise InvalidUserNameError("❌ UserName must contain digits or letters and between 4 and 12 characters")
    def validatePassword(self, password):
        if not (8 <= len(password) <= 20):
            raise InvalidPasswordError("❌ Password must be between 8 and 20 characters.")
        if not re.search(r'[A-Za-z]', password):
            raise InvalidPasswordError("❌ Password must include at least one letter.")
        if not re.search(r'\d', password):
            raise InvalidPasswordError("❌ Password must include at least one digit.")      