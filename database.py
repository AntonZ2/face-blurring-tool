import sqlite3
from tkinter import messagebox
# importing class from hashalg.py program
from hashalg import Hashing

# objects imported from my other python files
hash_function = Hashing()


class Database:
    def __init__(self):
        # connect the local sqlite database
        self.MyDB = sqlite3.connect("faces.db")

        # set the cursor to access the table
        self.MyCursor = self.MyDB.cursor()

        # creates the user table
        self.MyCursor.execute("CREATE TABLE IF NOT EXISTS tblUsers ("
                              "UserID INTEGER NOT NULL, "
                              "Username VARCHAR(255) NOT NULL, "
                              "Password VARCHAR(255) NOT NULL, "
                              "VideoSetting DECIMAL(5,10), "
                              "PhotoSetting DECIMAL(5,20), "
                              "PRIMARY KEY (UserID))")

        # creates the photo table in the database to save faces for photo blurring
        self.MyCursor.execute("CREATE TABLE IF NOT EXISTS tblPhoto ("
                              "PhotoID INTEGER NOT NULL, "
                              "UserID INTEGER NOT NULL, "
                              "PhotoFace MEDIUMBLOB NOT NULL, "
                              "PRIMARY KEY (PhotoID)"
                              "FOREIGN KEY (UserID) REFERENCES tblUsers (UserID))")

        # creates the video table in the database to save faces for video blurring
        self.MyCursor.execute("CREATE TABLE IF NOT EXISTS tblVideo ("
                              "VideoID INTEGER NOT NULL, "
                              "UserID INTEGER NOT NULL, "
                              "VideoFace MEDIUMBLOB NOT NULL, "
                              "PRIMARY KEY (VideoID)"
                              "FOREIGN KEY (UserID) REFERENCES tblUsers (UserID))")

        self.MyDB.commit()

        self.UserID = 0

        self.success = False

    # Method to ensure user disconnects from database when logged out
    def logout(self):
        self.UserID = 0

    # Method to login and search for user in database
    def find_user(self, username, password, usertype):
        # hashes inputted username and password
        username = hash_function.sha256(username)
        password = hash_function.sha256(password)
        if usertype == 'guest':
            self.UserID = 'guest'
        else:
            statement = f"SELECT * FROM tblUsers WHERE Username='{username}' AND Password = '{password}';"
            self.MyCursor.execute(statement)
            result = self.MyCursor.fetchone()
            # user was not found in the database or incorrect login data entered
            if not result:
                messagebox.showinfo("User Not Found", "User Not Found\n\n"
                                                      "Please make sure correct username and\n"
                                                      "password were entered and try again")
            else:
                self.UserID = result[0]
                self.success = True

    # Method to register a new user
    def register_user(self, username, password, password2):
        # password strength parameters checked
        weaknesses = 3
        if any('a' <= character <= 'z' for character in password):
            weaknesses -= 1
        if any('A' <= character <= 'Z' for character in password):
            weaknesses -= 1
        if any(character.isdigit() for character in password):
            weaknesses -= 1
        # check if username already exists in database
        username_statement = f"SELECT * FROM tblUsers WHERE Username='{hash_function.sha256(username)}'"
        self.MyCursor.execute(username_statement)
        if self.MyCursor.fetchone():
            # error message that username already in use
            messagebox.showinfo("Username already exists", "Username already exists\n\n"
                                                           "Please enter a new Username and retype passwords\n"
                                                           "and try again by pressing Register")
        # error message in username too long
        elif len(username) > 15:
            messagebox.showinfo("Username is too long", "Username is too long\n\n"
                                                        "Username should not exceed 15 characters in length")
        # error message if username too short
        elif len(username) < 3:
            messagebox.showinfo("Username is too short", "Username is too short\n\n"
                                                         "Username should not be less than 3 characters in length")
        # error message if password and retyped password do not match
        elif password != password2:
            messagebox.showinfo("Passwords do not match", "Passwords do not match\n\n"
                                                          "Please enter passwords again and press Register")
        # error message if password too short
        elif len(password) < 8:
            messagebox.showinfo("Password is too short", "Password is too short\n\n"
                                                         "Please ensure password is at least 8 characters long")
        # error message if password doesn't meet all strength requirements
        elif weaknesses != 0:
            messagebox.showinfo("Password does not meet all strength requirement",
                                "Password does not meet all strength requirement\n\n"
                                "Please ensure password contains\n"
                                "at least one lowercase character, "
                                "one uppercase character and"
                                "one numerical digit.")
        else:
            # If there are no errors new user is added to tblUsers in the database
            username = hash_function.sha256(username)
            password = hash_function.sha256(password)
            register_statement = f"INSERT INTO tblUsers(Username, Password, VideoSetting, PhotoSetting)" \
                                 f"VALUES ('{username}','{password}',8,8)"
            self.MyCursor.execute(register_statement)
            self.MyDB.commit()
            # registered successfully message shown and user is sent back to login screen
            messagebox.showinfo("Registered Successfully", "Registered Successfully\n\n "
                                                           "Login with your new account")
            self.success = True

    def success_check(self):
        x = self.success
        self.success = False
        return x

    # Method that finds the users last used video intensity
    def video_intensity_get(self):
        # if user is guest then default intensity is set
        if self.UserID == 'guest':
            return 8
        else:
            statement = f"SELECT * FROM tblUsers WHERE UserID = {self.UserID}"
            self.MyCursor.execute(statement)
            result = self.MyCursor.fetchone()
            return round(result[3])

    # Method that finds the users last used video blurring intensity
    def video_intensity_set(self, intensity):
        if self.UserID == 'guest':
            pass
        else:
            statement = f"UPDATE tblUsers SET VideoSetting = {intensity} WHERE UserID = {self.UserID}"
            self.MyCursor.execute(statement)
            self.MyDB.commit()

    # Method that finds the users last used photo blurring intensity
    def photo_intensity_get(self):
        # if user is guest then default intensity is set
        if self.UserID == 'guest':
            return 8
        else:
            statement = f"SELECT * FROM tblUsers WHERE UserID = {self.UserID}"
            self.MyCursor.execute(statement)
            result = self.MyCursor.fetchone()
            return round(result[4])

    # Method that saves last used blurring intensity of user to keep for later login and use
    def photo_intensity_set(self, intensity):
        if self.UserID == 'guest':
            pass
        else:
            statement = f"UPDATE tblUsers SET PhotoSetting = {intensity} WHERE UserID = {self.UserID}"
            self.MyCursor.execute(statement)
            self.MyDB.commit()

    # Method to insert face images to save for future if user ticks off save tick box
    def video_insert_images(self, filepaths):
        if self.UserID == 'guest':
            pass
        else:
            for i in filepaths:
                with open(i, "rb") as File:
                    binarydata = File.read()
                insert_blob_query = "INSERT INTO tblVideo (UserID,VideoFace) VALUES (?,?)"
                self.MyCursor.execute(insert_blob_query, (self.UserID, binarydata))
                self.MyDB.commit()

    # Method to insert face images to save for future if user ticks off save tick box
    def photo_insert_images(self, filepaths):
        if self.UserID == 'guest':
            pass
        else:
            for i in filepaths:
                with open(i, "rb") as File:
                    binarydata = File.read()
                insert_blob_query = "INSERT INTO tblPhoto (UserID,PhotoFace) VALUES (?,?)"
                self.MyCursor.execute(insert_blob_query, (self.UserID, binarydata))
                self.MyDB.commit()

    # Method to run sql query to retrieve current users saved face images to ignore in blurring
    def video_retrieve_images(self):
        if self.UserID == 'guest':
            pass
        else:
            sqlstatement2 = f"SELECT VideoFace FROM tblVideo WHERE UserID = {self.UserID}"
            self.MyCursor.execute(sqlstatement2)
            result = self.MyCursor.fetchall()
            for i in result:
                image = f"./ignore/saved{result.index(i)}.jpg"
                with open(image, "wb") as File:
                    File.write(i[0])
                    File.close()

    # Method to run sql query to retrieve current users saved face images to ignore in blurring
    def photo_retrieve_images(self):
        if self.UserID == 'guest':
            pass
        else:
            sqlstatement2 = f"SELECT PhotoFace FROM tblPhoto WHERE UserID = {self.UserID}"
            self.MyCursor.execute(sqlstatement2)
            result = self.MyCursor.fetchall()
            for i in result:
                image = f"./ignore/saved{result.index(i)}.jpg"
                with open(image, "wb") as File:
                    File.write(i[0])
                    File.close()

    # Method to run sql query to delete current users saved faces in photo table
    def photo_cleartable(self):
        delete_query = f"DELETE from tblPhoto WHERE UserID = {self.UserID}"
        self.MyCursor.execute(delete_query)
        self.MyDB.commit()

    # Method to run sql query to delete current users saved faces in video table
    def video_cleartable(self):
        delete_query = f"DELETE from tblVideo WHERE UserID = {self.UserID}"
        self.MyCursor.execute(delete_query)
        self.MyDB.commit()
