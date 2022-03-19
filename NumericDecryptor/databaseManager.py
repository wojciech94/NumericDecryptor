import sqlite3


class DatabaseManager:
    def __init__(self):
        self.db_path = 'pindecryptor.db'
        self.table_name = 'Decrypto'
        cond = DatabaseValidator.validate_database(self.db_path, self.table_name)
        if not cond:
            self.create_table()

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
        except ConnectionError:
            print("Cannot create table")

    def insert_record(self, uid, nick, public_key, n):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Decrypto")
        empty_table = cursor.fetchone() is None
        next_id = 0
        if not empty_table:
            cursor.execute("Select Id FROM Decrypto WHERE Id = {}".format(uid))
            if cursor.fetchone() is not None:
                # set next id as max (id) +1
                cursor.execute("SELECT Id FROM Decrypto WHERE Id  = (SELECT MAX(Id) FROM Decrypto)")
                next_id = cursor.fetchone()[0] + 1
            else:
                # if id not in database insert record with selected id
                next_id = uid
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

    def get_record(self, uid):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT PublicKey,KeyRange FROM Decrypto WHERE Id = {}".format(uid))
        values = cursor.fetchone()
        conn.close()
        return values

    def get_records(self, asc=True):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        order = 'ASC' if asc else 'DESC'
        cursor.execute("SELECT * FROM Decrypto ORDER BY Id {}".format(order))
        results = cursor.fetchall()
        conn.close()
        return results


class DatabaseValidator:
    @staticmethod
    def validate_database(path: str, name: str):  # Check is table (name) exist in db path
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        exist_query = "SELECT count(name) FROM sqlite_master WHERE type = 'table' AND name = '{}'".format(name)
        cursor.execute(exist_query)
        fetch = cursor.fetchone()
        is_table_exist = False
        if fetch is not None and fetch[0] != 0:
            is_table_exist = True
        conn.close()
        return is_table_exist
