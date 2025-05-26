from controllers.UserController import UserController
from controllers.BookController import BookController
from core.ErrorHandling import( 
    UserNotFoundError,
    InvalidCredentialsError,
    UsernameAlreadyExistsError,
    InvalidPasswordError,
    InvalidUserNameError,
    InvalidNameOrLastNameError,
    BookAlreadyExistsError,
    BookNotFoundError
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
        profileData = self.user.getProfile()
        name = profileData["name"]
        lastName = profileData["lastName"]
        if name is None:
            return self.setName()
        print(f"Hi dear {name + ' ' + lastName if lastName is not None else name}")
        text = "Please choose a command from the list below:\n1. Show my books\n2. Profile\n3. Borrow Book\n" + ("4. Admin Panel\n" if profileData["isAdmin"] else '') + "0. Log out\nEnter the number of your choice:\n>>> "
        while True:
            userChoice = input(text).strip()
            match userChoice:
                case '1':
                    return self.showMyBooks()
                case '2':
                    return self.profile()
                case '3':
                    return self.borrowBook()
                case '4':
                    if profileData["isAdmin"]:
                        return self.adminPanel()
                    else:
                        print("Invalid Input. try again")
                case '0':
                    return
                case _:
                    print("Invalid Input. try again")
    
    def showMyBooks(self):
        books = self.user.getBooks()
        if books:
            print("\n📚 Your Borrowed Books:\n")
            for index, book in enumerate(books, 1):
                print(f"{index}. Book ID   : {book['bookId']}")
                print(f"   Status    : {book['status']}")
                print(f"   From      : {book['from']}")
                print(f"   To        : {book['to'] if book['to'] else 'Not returned yet'}")
                print(f"   Privacy   : {'Private' if book['privacy'] else 'Public'}")
                print("-" * 40)
        else:
            print("you dont have any book history yet")
            print("-" * 40)
            return self.mainMenu()
        
    def profile(self):
        profileData = self.user.getProfile()
        print("\n👤 Your Profile Information")
        print(f"UserName     : {profileData["userName"]}")
        print(f"Name         : {profileData["name"]}")
        print(f"Last Name    : {profileData["lastName"]}")
        print(f"Email        : {profileData["email"]}")
        print(f"Phone Number : {profileData["phoneNumber"]}")
        print(f"Age          : {profileData["age"]}")
        print("Addresses:")
        addresses = profileData["addresses"]
        if addresses:
            for label, addr in addresses.items():
                print(f"  {label}: {addr['country']}, {addr['city']}, {addr['address']}")
        else:
            print("  No addresses added yet.")

        print("\nDo you want to update your profile? (yes/no)")
        choice = input(">>> ").strip().lower()
        if choice != "yes":
            return self.mainMenu()

        while True:
            print("\nWhat would you like to update?")
            print("1. Name")
            print("2. Last Name")
            print("3. Email")
            print("4. Phone Number")
            print("5. Age")
            print("6. Add Address")
            print("7. Username")
            print("0. Back to Main Menu")

            option = input(">>> ").strip()
            match option:
                case "1":
                    self.user.updateName(input("Enter new name: ").strip())
                case "2":
                    self.user.updateLastName(input("Enter new last name: ").strip())
                case "3":
                    self.user.updateEmail(input("Enter new email: ").strip())
                case "4":
                    self.user.updatePhoneNumber(input("Enter new phone number: ").strip())
                case "5":
                    self.user.updateAge(input("Enter new age: ").strip())
                case "6":
                    label = input("Address label (e.g., home, office): ").strip()
                    country = input("Country: ").strip()
                    city = input("City: ").strip()
                    address = input("Full address: ").strip()
                    self.user.addAddress(label, country, city, address)
                case "7":
                    try:
                        self.user.updateUserName(input("Enter new userName: ").strip())
                    except UsernameAlreadyExistsError as e:
                        print(e)
                case "0":
                    return self.mainMenu()
                case _:
                    print("❌ Invalid option. Please try again.")
                    continue

            print("✅ Profile updated successfully.")
    
    def adminPanel(self):
        profileData = self.user.getProfile()
        while True:
            print("\n🛠️ Admin Panel")
            print("1. manage users")
            print("2. Manage Books")
            print("0. Back to Main Menu")

            choice = input(">>> ").strip()

            match choice:
                case "1":
                    if profileData["manageUsers"]:
                        return self.manageUsers()
                    else:
                        print("Access denied")
                        return self.adminPanel()
                case "2":
                    if profileData["addingBooks"] or profileData["removingBooks"] or profileData["editingBooks"]:
                        return self.manageBooks()
                    else:
                        print("Access denied")
                        return self.adminPanel()
                case "0":
                    return self.mainMenu()
                case _:
                    print("❗ Invalid choice. Please try again.")
                    return self.adminPanel()

    def manageUsers(self):
        print("\n🔧 Manage Users")
        userId = input("Enter the User ID: ").strip()
        if not userId.isdigit():
            print("❌ Invalid User ID format. It should be a number.")
            return

        user = self.user.getUserById(userId)
        if not user:
            print("❌ User not found.")
            return

        profileData = user.getProfile()
        print("\n👤 User Information")
        print(f"UserID      : {userId}")
        print(f"Username    : {profileData["userName"]}")
        print(f"Name        : {profileData["name"]} {profileData['lastName'] if profileData['lastName'] is not None else '' }")
        print(f"Email       : {profileData["email"]}")
        print(f"Phone       : {profileData["phoneNumber"]}")
        print(f"Age         : {profileData["age"]}")
        print(f"Active      : {profileData["isActive"]}")
        print(f"Admin       : {profileData["isAdmin"]}")
        print(f"Created At  : {profileData["createdAt"]}")
        print(f"Addresses   :")
        addresses = user.getAddresses()
        if addresses:
            for label, addr in addresses.items():
                print(f"  {label}: {addr['country']}, {addr['city']}, {addr['address']}")
        else:
            print("  No addresses.")
        while True:
            print("\nWhat do you want to do with this user?")
            print("1. Deactivate user")
            print("2. Activate user")
            print("3. Promote to admin")
            print("4. Demote from admin")
            print("0. Back")

            admin = self.user.getProfile()

            choice = input(">>> ").strip()
            match choice:
                case "1":
                    user.setActive(False)
                    print("🚫 User deactivated.")
                case "2":
                    user.setActive(True)
                    print("✅ User activated.")
                case "3":
                    if admin["manageAdmins"]:
                        user.setAdmin(True)
                        print("🛡️ User promoted to admin.")
                        return self.setPermissions(user)
                    else:
                        print("Access Denied")
                case "4":
                    if admin["manageAdmins"]:
                        user.setAdmin(False)
                        print("⚠️ User demoted from admin.")
                    else:
                        print("Access Denied")
                case "0":
                    return
                case _:
                    print("❌ Invalid choice.")

    def setPermissions(self,user):
        print("\n🔒 Set Admin Permissions")

        permission_labels = {
            "addingBooks": "📚 Add Books",
            "editingBooks": "✏️ Edit Books",
            "removingBooks": "🗑️ Remove Books",
            "manageUsers": "👥 Manage Users",
            "manageAdmins": "🛡️ Manage Admins",
            "viewReports": "📊 View Reports"
        }

        print("Toggle permissions (y = yes, n = no):")

        for key, label in permission_labels.items():
            curentPermission = user.getProfile()[key]
            default = "y" if curentPermission else "n"
            userInput = input(f"{label} [{default}]: ").strip().lower()
            if userInput not in ['y','n']: userInput == default
            if userInput == 'y': 
                user.setPermission(key,True)
            else:
                user.setPermission(key,False)
                
        print("✅ Permissions updated successfully.")


    def manageBooks(self):
        while True:
            print("\n📚 Book Management Menu:")
            print("1. Add a new book")
            print("2. View book details")
            print("3. Update a book")
            print("4. Delete a book")
            print("0. Back to main menu")

            choice = input("Enter your choice: ").strip()

            match choice:
                case "1":
                    return self.addBook()
                case "2":
                    return self.bookDetails()
                case "3":
                    return self.updateBook()
                case "4":
                    return self.deleteBook()
                case "0":
                    return
                case _:
                    print("❌ Invalid choice.")

    
    def addBook(self):
        bookId = input("Enter Book ID: ")
        title = input("Title: ")
        author = input("Author: ")
        publisher = input("Publisher: ")
        publishYear = input("Publish Year: ")
        abstract = input("Abstract: ")
        pages = input("Pages: ")
        language = input("Language: ")
        contentType = input("Content Type: ")
        usageType = input("Usage Type: ")
        genres = input("Genres (comma-separated): ").split(',')
        availableCopies = input("Available Copies: ")
        totalCopies = input("Total Copies: ")

        bookInfo = [
            title, author, publisher, publishYear, abstract,
            pages, language, contentType, usageType, genres,
            availableCopies, totalCopies
        ]
        try:
            BookController.addBook(bookId, bookInfo)
            print("✅ Book added successfully.")
            return self.mainMenu()
        except BookAlreadyExistsError as e:
            print(f"❌ Error: {e}")
            return self.addBook()

    def bookDetails(self):
        bookId = input("Enter Book ID to view: ")
        try:
            bookController = BookController.getBook(bookId)
            details = bookController.getDetails()
            for key, value in details.items():
                print(f"{key}: {value}")
                return self.mainMenu()
        except Exception as e:
            print(f"❌ Error: {e}")

    def updateBook(self):
        bookId = input("Enter Book ID to update: ")
        try:
            bookController = BookController.getBook(bookId)
            print("Which field do you want to update?")
            print("1. Title\n2. Author\n3. Publisher\n4. Publish Year\n5. Abstract\n6. Pages")
            print("7. Language\n8. Content Type\n9. Usage Type\n10. Genres")
            print("11. Available Copies\n12. Total Copies\n13. Premium")
            field = input("Enter field number: ").strip()
            value = input("Enter new value: ")

            update_methods = {
                '1': bookController.updateTitle,
                '2': bookController.updateAuthor,
                '3': bookController.updatePublisher,
                '4': bookController.updatePublishYear,
                '5': bookController.updateAbstract,
                '6': lambda v: bookController.updatePages(int(v)),
                '7': bookController.updateLanguage,
                '8': bookController.updateContentType,
                '9': bookController.updateUsageType,
                '10': lambda v: bookController.updateGenres(v.split(',')),
                '11': lambda v: bookController.updateAvailableCopies(int(v)),
                '12': lambda v: bookController.updateTotalCopies(int(v))
            }
            if field in update_methods:
                update_methods[field](value)
                print("✅ Book updated successfully.")
            else:
                print("❌ Invalid field number.")
            
            return self.updateBook()
        except BookNotFoundError as e:
            print(f"❌ Error: {e}")
            return self.updateBook()

    def deleteBook(self):
        bookId = input("Enter Book ID to delete: ")
        try:
            BookController.deleteBook(bookId)
            print("✅ Book deleted.")
            return self.mainMenu()
        except Exception as e:
            print(f"❌ Error: {e}")

    def borrowBook(self):
        userInput = input("Enter the Book ID you want to borrow: \nOr back for going to main menu\n").strip()
        if userInput == 'back':
            return 'back'
        try:
            bookId = userInput
            bookController = BookController.getBook(bookId)
            book = bookController.getDetails()
            availableCopies = book["availableCopies"]

            if availableCopies == 0:
                print("❌ No available copies to borrow.")
                return self.borrowBook()
            else:
                bookController.updateAvailableCopies(int(availableCopies)-1)


            self.user.addBook(bookId)

            print(f"✅ Book '{book["title"]}' borrowed successfully.")

        except BookNotFoundError:
            print("❌ Book not found.")
            return self.borrowBook()

        return self.mainMenu()