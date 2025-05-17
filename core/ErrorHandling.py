class AppError(Exception):
    def __init__(self,message,code=None):
        self.message = message
        self.code = code
    def __str__(self):
        return f"[{self.code}] {self.message}" if self.code else self.message
    
class UserNotFoundError(AppError):
    def __init__(self, message, code=None):
        super().__init__(message, code)

class InvalidCredentialsError(AppError): # for checking the passoword user enters with the password in database
    def __init__(self, message, code=None):
        super().__init__(message, code)

class UsernameAlreadyExistsError(AppError):
    def __init__(self, message, code=None):
        super().__init__(message, code)

class InvalidPasswordError(AppError): # For checking syntax of password when user sign up
    def __init__(self, message, code=None):
        super().__init__(message, code)

class InvalidUserNameError(AppError):
    def __init__(self, message, code=None):
        super().__init__(message, code)