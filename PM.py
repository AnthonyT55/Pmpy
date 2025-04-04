from getpass import getpass
import sys, string, random, sqlite3
from utils import *


class PassMan:
    def __init__(self):
        pass

    def Options(self):
        clearScreen()
        self.Border()
        print("PassMan Menu")
        print("1: Add Credentials")
        print("2: Show Credentials")
        print("3: Generate Password")
        print("4: Delete Credentials")
        print("5: Exit")
        

        choice = input("Enter your choice: ")
        match choice:
            case '1':
                print("ADDING CREDENTIALS...")
                clearScreen()
                self.addcredentials()

            case '2':
                print("SHOWING CREDENTIALS...")
                clearScreen()
                self.showcredentials()

            case '3':
                print("GENERATING A NEW PASSWORD")
                clearScreen()
                pw = self.generatePW()
                print("GENERATED PASSWORD: " + pw + "\nMAKE SURE TO COPY THIS PASSWORD IF YOU WISH TO SAVE IT, I DO NOT WANT TO REMEMBER ANYTHING")
                    
                

            case '4':
                print("DELETING CREDENTIALS")
                clearScreen()
                self.deletecredentials()

            case '5':
                clearScreen()
                print("Goodbye")
                sys.exit(0)
            
            case _ :
                clearScreen()
                print("Goodbye")
                sys.exit(0)

        self.rerun()


    def test(self):
        #country = input("COUNTRY: ")
        #state = input("STATE: ")
        #city = input("CITY: ")
        #organizationname = input("NAME OF ORGANIZATION: ")
        #commonname = input("PRODUCT NAME: ")
        #PassMan.Options(self)
        #data = getpass("Enter a decryption key: ")
        #print(getsecretkeyfromstring(data))
        #if(getsecretkeyfromstring("password") == getsecretkeyfromstring(data)):
        #    self.Options()
        self.Border()
        #pw = getpass("Enter Your Password: ")
        #generatekeys(pw)
        #generateCert(country, state, city, organizationname, commonname)
        self.createDB()
        self.addcredentials()
        self.showcredentials()
        #print(self.createDB())
        
        
       

    def Border(self):
        print("__________                         _____                 ")
        print("\\______   \\_____    ______ ______ /     \\ _____    ____  ")
        print(" |     ___/\\__  \\  /  ___//  ___//  \\ /  \\\\__  \\  /    \\ ")
        print(" |    |     / __ \\_\\___ \\ \\___ \\/    Y    \\/ __ \\|   |  \\")
        print(" |____|    (____  /____  >____  >____|__  (____  /___|  /")
        print("                \\/     \\/     \\/        \\/     \\/     \\/ ")
        print("")


    def generatePW(self):
        characters = string.ascii_letters + string.digits + string.punctuation
        pw = "".join(random.choices(list(characters), k = 32))
        #print(pw)
        return pw

    def createDB(self):
        if os.path.exists("Vault/Pm.db"):
            pass
        else:
            self = sqlite3.connect("Vault/Pm.db")
            cursor = self.cursor()
            cursor.execute("CREATE TABLE actor(number, uname, pword, platform)")
            res = cursor.execute("SELECT name FROM sqlite_master")
            return res.fetchone()
    
    def addcredentials(self):
        index = 1
        username = input("Enter username to add: ")
        password = input("Enter the associated password: ")
        platform = input("Enter the platform this information is for: ")
        
        self = sqlite3.connect("Vault/Pm.db")
        cursor = self.cursor()
        for row in cursor.execute("SELECT * FROM actor"):
            index += 1

        data = (index, encryptData(username), encryptData(password), (platform))
        cursor.execute("INSERT INTO actor VALUES(?, ?, ?, ?)", data)
        self.commit()
        self.close()

    def showcredentials(self):
        decryptionpw = getpass("Enter your decryption key: ")
        self = sqlite3.connect("Vault/Pm.db")
        cursor = self.cursor()
        for row in cursor.execute("SELECT number, uname, pword, platform FROM actor"):
            data = list(row)
            decryptedData = [data[0], decryptData(data[1], decryptionpw), decryptData(data[2], decryptionpw), data[3]]
            print("\nUser Index: " + str(decryptedData[0]) + "\nUsername: " + str(decryptedData[1]) + "\nPassword: " + str(decryptedData[2]) + "\nPlatform: " + str(decryptedData[3]))
        self.close()


    def deletecredentials(self):
        index = input("Enter the index of credentials you with to delete: ")
        self = sqlite3.connect("Vault/Pm.db")
        cursor = self.cursor()
        cursor.execute("DELETE FROM actor WHERE number = ?", index).rowcount
        self.commit()
        self.close()
            


    def run(self):
        clearScreen()
        self.Border()


        
        if os.path.exists("Vault/rsa.pem"):
            print("PRIVATE KEY EXISTS, GENERATION UNNECESSARY...")
            print("STARTING PASSMAN")
            self.createDB()
            self.Options()
        else:
            print("PRIVATE KEYS DON'T EXIST, BEGINNING USER REGISTRATION...")
            generatekeys()
            self.createDB()
            self.Options()


    def rerun(self):
        choose = input("\nWould you like to rerun Passman?\n'1' for yes, '2' for no: ")
        if choose == "1":
            self.Options()
        else:
            sys.exit(0)


        


