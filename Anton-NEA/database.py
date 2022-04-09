import sqlite3
from tkinter import messagebox

# objects imported from my other python files
from hashalg import Hashing
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

    def logout(self):
        self.UserID = 0

    def find_user(self, username, password, usertype):
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
                messagebox.showinfo("User Not Found", "User Not Found\n"
                                                      "Please make sure correct username and\n"
                                                      "password were entered and try again")
            else:
                self.UserID = result[0]

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
        username_statement = f"SELECT * FROM tblUsers WHERE Username='{username}'"
        self.MyCursor.execute(username_statement)
        if self.MyCursor.fetchone():
            messagebox.showinfo("Username already exists", "Username already exists\n"
                                                           "Please enter a new Username and retype passwords\n"
                                                           "and try again by pressing Register")
        elif len(username) > 15:
            messagebox.showinfo("Username is too long", "Username is too long\n"
                                                        "Username should not exceed 15 characters in length")

        elif password != password2:
            messagebox.showinfo("Passwords do not match", "Passwords do not match\n"
                                                          "Please enter passwords again and press Register")

        elif len(password) < 8:
            messagebox.showinfo("Password is too short", "Password is too short\n"
                                                         "Please ensure password is at least 8 characters long")
        elif weaknesses != 0:
            messagebox.showinfo("Password does not meet all strength requirement",
                                "Password does not meet all strength requirement\n"
                                "Please ensure password contains\n"
                                "at least one lowercase character, "
                                "one uppercase character and"
                                "one numerical digit.")
        else:
            username = hash_function.sha256(username)
            password = hash_function.sha256(password)
            register_statement = f"INSERT INTO tblUsers(Username, Password, VideoSetting, PhotoSetting)" \
                                 f"VALUES ('{username}','{password}',8,8)"
            self.MyCursor.execute(register_statement)
            self.MyDB.commit()
            messagebox.showinfo("Registered Successfully", "Registered Successfully\n "
                                                           "Press the back button to return to Login screen\n"
                                                           "and login with your account details.")

    # finds the users last used video intensity
    def video_intensity_get(self):
        # if user is guest then default intensity is set
        if self.UserID == 'guest':
            return 8
        else:
            statement = f"SELECT * FROM tblUsers WHERE UserID = {self.UserID}"
            self.MyCursor.execute(statement)
            result = self.MyCursor.fetchone()
            return round(result[3])

    def video_intensity_set(self, intensity):
        if self.UserID == 'guest':
            pass
        else:
            statement = f"UPDATE tblUsers SET VideoSetting = {intensity} WHERE UserID = {self.UserID}"
            self.MyCursor.execute(statement)
            self.MyDB.commit()

    # finds the users last used video intensity
    def photo_intensity_get(self):
        # if user is guest then default intensity is set
        if self.UserID == 'guest':
            return 8
        else:
            statement = f"SELECT * FROM tblUsers WHERE UserID = {self.UserID}"
            self.MyCursor.execute(statement)
            result = self.MyCursor.fetchone()
            return round(result[4])

    def photo_intensity_set(self, intensity):
        if self.UserID == 'guest':
            pass
        else:
            statement = f"UPDATE tblUsers SET PhotoSetting = {intensity} WHERE UserID = {self.UserID}"
            self.MyCursor.execute(statement)
            self.MyDB.commit()

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

    def photo_cleartable(self):
        delete_query = f"DELETE from tblPhoto WHERE UserID = {self.UserID}"
        self.MyCursor.execute(delete_query)
        self.MyDB.commit()

    def video_cleartable(self):
        delete_query = f"DELETE from tblVideo WHERE UserID = {self.UserID}"
        self.MyCursor.execute(delete_query)
        self.MyDB.commit()
