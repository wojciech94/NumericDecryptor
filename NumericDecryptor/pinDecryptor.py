import random
from databaseManager import DatabaseManager


class PinDecryptor:
    def __init__(self):
        self.databasemanager = DatabaseManager()

    def generate_identity(self):
        n, t = self.initialize_nt()
        e = self.generate_public_key(t)
        d = self.generate_private_key(e, t)
        print('n:' + str(n))
        print("e:" + str(e))
        print('d:'+str(d))

    def initialize_nt(self):
        p = int(input("Type p:"))
        q = int(input("Type q:"))
        n = p * q
        t = (p - 1) * (q - 1)
        return n, t

    def nwd(self, a, b):
        while a != b:
            if a > b:
                a -= b
            else:
                b -= a
        return a

    def generate_public_key(self, toc):
        i = 0
        num = 2
        tab = []
        while i < 4 or num < toc:
            if self.nwd(num, toc) == 1:
                i += 1
                tab.append(num)
            num += 1
        return tab[random.randint(0, 4)]

    def generate_private_key(self, e, toc):
        i = 1
        while True:
            if (i*e) % toc == 1:
                return i
            i += 1

    def generate_cipher(self):
        e = int(input('Type public key:'))
        n = int(input('Type n value'))
        s = n+1
        while s > n:
            s = int(input('Type numeric cipher(lower than n)'))
        v = s**e % n
        print('Cypher:'+str(v))
        return v

    def decrypt_cipher(self):
        n = int(input('Type your n value:'))
        p = int(input('Type your private key:'))
        cypher = int(input('Type cypher:'))
        v = cypher**p % n
        print('Decrypted cypher:'+str(v))
        return v

    def add_user(self):
        nick = input("Type nick name:")
        p = input("type public key:")
        n = input("type n:")
        self.databasemanager.insert_record(nick, p, n)

    def delete_user(self):
        idd = input("Type id to delete")
        self.databasemanager.delete_record(idd)

    def print_database(self):
        self.databasemanager.print_all()

    def switch_loop(self):
        print("""Choose action:
1 - Add User
2 - Print Database
3 - Delete User
4 - Generate your Identity key
5 - Generate cypher
6 - Decrypt cypher
0 - Close program\n""")
        cond = input()
        match cond:
            case '1':
                self.add_user()
                return 1
            case '2':
                self.print_database()
                return 2
            case '3':
                self.delete_user()
                return 3
            case '4':
                self.generate_identity()
                return 4
            case '5':
                self.generate_cipher()
                return 5
            case '6':
                self.decrypt_cipher()
                return 6
            case '0':
                return 0
