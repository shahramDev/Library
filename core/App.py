from controllers.UserController import UserController
from controllers.AdminController import AdminController
from controllers.BookController import BookController
from core.ErrorHandling import( 
    UserNotFoundError,
    InvalidCredentialsError,
    UsernameAlreadyExistsError,
    InvalidPasswordError,
    InvalidUserNameError,
    InvalidNameOrLastNameError
)

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
        try:
            self.user = UserController.signIn(userName,password)
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
        try:
            self.user = UserController.signUp(userName,password)
            return self.setName()
        except UsernameAlreadyExistsError as e:
            return self.signUp("❌ Username already exists")
        except InvalidUserNameError as e:
            return self.signUp("❌ Invalid username\nUsername must be 4 to 12 characters and contain only letters, digits, or underscores\n")
        except InvalidPasswordError as e:
            return self.signUp("❌ Invalid password Password must be 8 to 20 characters, and contain at least one digit and one letter.\n")
        
    def setName(self,text="For continuing you've to set your name and lastname(optional) or send back to get to the first page\nwrite them in this format\nname lastname(optional) each one should be from 3 to 15 characters\n"):
        userInput = input(text)
        if userInput == 'back':
            return 'back'
        else:
            userInfo = userInput.split()
            try:
                self.user.setName(userInfo)
                return self.mainMenu()
            except InvalidNameOrLastNameError as e:
                return self.setName(e+"\n")
            
    def mainMenu(self):
        name = self.user.user.name
        lastName = self.user.user.lastName
        if name is None:
            return self.setName()
        print(f"Hi dear {name + ' ' + lastName if lastName is not None else name}")
        userChoice = input("Please choose a command from the list below:\n1. Show my books\n2. Profile\n3. MemberShip\n4. settings\n5. Log out\nEnter the number of your choice:\n")
        match userChoice:
            case '1':
                return self.showMyBooks()
            case '2':
                return self.profile()
            case '3':
                return self.membership()
            case '4':
                return self.settings()
            case '5':
                return
    def showMyBooks(self):
        pass
    def profile(self):
        pass
    def membership(self):
        pass
    def settings(self):
        pass