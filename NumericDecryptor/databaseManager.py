import sqlite3

class DatabaseManager:
    def __init__(self):
        self.db_path = "pindecryptor.db"
        self.validate_db()


    def validate_db(self):
        try:
            if not self.check_table_existance():
                self.create_table()
        except FileNotFoundError:
            print("DbNotConnected")

    def check_table_existance(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        exist_query = "SELECT count(name) FROM sqlite_master WHERE type = 'table' AND name = 'Decrypto'"
        cursor.execute(exist_query)
        if cursor.fetchone()[0] == 1:
            conn.close()
            print("Table exist")
            return True
        else:
            conn.close()
            print("Table not exist")
            return False

    def create_table(self):
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute('''CREATE TABLE Decrypto(
            ID INT PRIMARY KEY NOT NULL,
            Nick TEXT NOT NULL,
            PublicKey INT NOT NULL,
            KeyRange INT NOT NULL)''')
            connection.close()
            print("Table created")
        except ConnectionError:
            print("Cannot create table")

    def insert_record(self, nick, public_key, n):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Decrypto")
        empty_table = cursor.fetchone() is None
        next_id = 0
        if not empty_table:
            cursor.execute("SELECT Id FROM Decrypto WHERE Id  = (SELECT MAX(Id) FROM Decrypto)")
            next_id = cursor.fetchone()[0] + 1
        data = (next_id, nick, public_key, n)
        query = "INSERT INTO Decrypto Values(?, ?, ?, ?)"
        cursor.execute(query, data)
        conn.commit()
        conn.close()

    def delete_record(self, uid):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("Delete FROM Decrypto WHERE Id = {}".format(uid))
        conn.commit()
        conn.close()

    def print_all(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Decrypto")
        print(cursor.fetchall())
        conn.close()