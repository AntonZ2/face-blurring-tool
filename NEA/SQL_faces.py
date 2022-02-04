import sqlite3

# connect the local sqlite database
MyDB = sqlite3.connect("faces.db")


# set the cursor to access the table
MyCursor = MyDB.cursor()


# creates the image table in the database
MyCursor.execute("CREATE TABLE IF NOT EXISTS Images (id INTEGER NOT NULL PRIMARY KEY, "
                 "face MEDIUMBLOB NOT NULL)")


# inserts the images of faces uploaded by user if save checkbox is ticked
def insert_images(filepaths):
    for i in filepaths:
        with open(i, "rb") as File:
            binarydata = File.read()
        sqlite_insert_blob_query = """ INSERT INTO Images (face) VALUES (?)"""
        MyCursor.execute(sqlite_insert_blob_query, (binarydata, ))
        MyDB.commit()

# when a user blurs an image, all saved faces are retrieved and not blurred
def retrieve_images():
    sqlstatement2 = "SELECT face FROM Images"
    MyCursor.execute(sqlstatement2)
    result = MyCursor.fetchall()
    for i in result:
        image = f"./ignore/saved{result.index(i)}.jpg"
        with open(image, "wb") as File:
            File.write(i[0])
            File.close()

# clears all the saved faces from the database if user presses clear table button on GUI
def cleartable():
    delete_query = """DELETE from Images"""
    MyCursor.execute(delete_query)
    MyDB.commit()
