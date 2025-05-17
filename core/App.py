from controllers.UserController import UserController
from controllers.AdminController import AdminController
from controllers.BookController import BookController
from core.ErrorHandling import UserNotFoundError ,InvalidCredentialsError,UsernameAlreadyExistsError ,InvalidPasswordError ,InvalidUserNameError

import re

class App:
    def start(self):
        userChoice = input("For continuing you need to sign in or sign up\n1- sign in\n2- sign up\n3- exit\nsend the number of your choice\n")
        if userChoice == '1': # sign in
            response = self.signIn()
            if response == 'back':
                return self.start()
            return response
        elif userChoice == '2': # sign up
            response = self.signUp()
            if response == 'back':
                return self.start()
            return response
        elif userChoice == '3': # exit
            return
        else: # wrong answer
            return self.start()
    def signIn(self,text="please enter your username and passwrod in this format\nusername password\nsend back for going back\n"):
        userInput = input(text)
        if userInput == 'back':
            return 'back'
        userInfo = userInput.split()
        if len(userInfo) != 2:
            return self.signIn("make sure youre correct and try again. write your data in this format\nusername password\n")
        userName , password = userInfo
        userController = UserController()
        try:
            userController.getUser(userName).checkUser(password)
            self.userName = userName
            response = self.mainMenu()
            if response == 'back':
                return self.signIn()
            return response
        except UserNotFoundError:
            return self.signIn("❌ No such user. Please try again or type 'back' to return.\nusername password\n")
        except InvalidCredentialsError:
            return self.signIn("❌ Invalid password. Please try again or type 'back' to return.\nusername password\n")
    def signUp(self,text="please enter your username and passwrod in this format\nusername password\nsend back for going back\n"):
        userInput = input(text)
        if userInput == 'back':
            return 'back'
        userInfo = userInput.split()
        if len(userInfo) != 2:
            return self.signUp("make sure you're correct and try again. write your data in this format\nusername password\n")
        userName , password = userInfo
        userController = UserController()
        try:
            userController.signUp(userName,password)
            self.userName = userName
            return self.getName()
        except UsernameAlreadyExistsError as e:
            return self.signUp("❌ Username already exists")
        except InvalidUserNameError as e:
            return self.signUp("❌ Invalid username\nUsername must be 4 to 12 characters and contain only letters, digits, or underscores\n")
        except InvalidPasswordError as e:
            return self.signUp("❌ Invalid password Password must be 8 to 20 characters, and contain at least one digit and one letter.\n")
    def getName(self):
        userInput = input("For continuing you've to set your name and lastname(optional) or send back to get to the first page\nwrite them in this format\nname lastname(optional)\n")
        if userInput == 'back':
            return 'back'
        else:
            userInfo = userInput.split()
            if len(userInfo) in [1,2] and all(list(map(lambda text: re.fullmatch(r'\w{3,9}',text),userInfo))):
                userController = UserController()
                UserController.setName(self.userName,userInfo)
                return self.mainMenu()
            return self.getName()
    def mainMenu(self):
        user = UserController().getUser(self.userName).user
        print(f"Hi dear {user['name'] + ' ' + user['lastName'] if user.get('lastName') else user['name']}")