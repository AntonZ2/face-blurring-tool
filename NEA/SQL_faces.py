import sqlite3

MyDB = sqlite3.connect("faces.db")

MyCursor = MyDB.cursor()

MyCursor.execute("CREATE TABLE IF NOT EXISTS Images (id INTEGER NOT NULL PRIMARY KEY, "
                 "face MEDIUMBLOB NOT NULL)")


def insert_images(filepaths):
    for i in filepaths:
        with open(i, "rb") as File:
            binarydata = File.read()
        sqlite_insert_blob_query = """ INSERT INTO Images (face) VALUES (?)"""
        MyCursor.execute(sqlite_insert_blob_query, (binarydata, ))
        MyDB.commit()


def retrieve_images():
    sqlstatement2 = "SELECT face FROM Images"
    MyCursor.execute(sqlstatement2)
    result = MyCursor.fetchall()
    for i in result:
        image = f"./ignore/saved{result.index(i)}.jpg"
        with open(image, "wb") as File:
            File.write(i[0])
            File.close()


