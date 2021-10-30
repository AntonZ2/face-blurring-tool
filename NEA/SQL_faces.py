import sqlite3

MyDB = sqlite3.connect("faces.db")

MyCursor = MyDB.cursor()

MyCursor.execute("CREATE TABLE IF NOT EXISTS Images (id INTEGER NOT NULL PRIMARY KEY, "
                 "face MEDIUMBLOB NOT NULL)")


def insert_images(filepaths):
    for i in filepaths:
        with open(i, "rb") as File:
            binarydata = File.read()
        MyCursor.execute("""INSERT INTO Images (face) VALUES(:binarydata)""", (binarydata, ))
        MyDB.commit()


def retrieve_images():
    sqlstatement2 = "SELECT * FROM Images"
    MyCursor.execute(sqlstatement2)
    result = MyCursor.fetchall()
    for i in result[1]:
        if type(i) != int:
            image = f"./main/{}.jpg"
            with open(image, "wb") as File:
                File.write(i)
                File.close()


paths = ['jeff.jpeg', '0.jpg']
# insert_images(paths)
retrieve_images()
