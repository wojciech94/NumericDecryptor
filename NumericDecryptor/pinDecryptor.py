from random import randint
from databaseManager import DatabaseManager


class PinDecryptor:
    def __init__(self):
        self.databasemanager = DatabaseManager()
        self.public_key = None
        self.cypher_range = None
        self.init_identificator()

    def init_identificator(self):
        try:
            with open('myidentificator.txt', 'r') as f:
                lines = f.readlines()
                count = sum(1 for line in lines)
                if count == 2:
                   self.public_key = lines[0].rsplit()[0]
                   self.cypher_range = lines[1]
        except FileNotFoundError:
            self.public_key = 'xxx'
            self.cypher_range = 'xxxx'

    def update_identificator(self, public_key, cypher_range):
        self.public_key = public_key
        self.cypher_range = cypher_range
        f = open('myidentificator.txt', 'w')
        f.writelines('{0}\n{1}'.format(self.public_key, self.cypher_range))
        f.close()

    def generate_identity(self, ran):
        ran = int(ran)
        n, t = self.initialize_nt(ran)
        pub = self.generate_public_key(t)
        priv = self.generate_private_key(pub, t)
        self.update_identificator(pub, n)
        return pub, priv, n

    def initialize_nt(self, ran):
        p = q = 0
        while p*q < ran:
            p = randint(2, 200)
            q = randint(2, 200)
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
        return tab[randint(0, 4)]

    def generate_private_key(self, e, toc):
        i = 1
        while True:
            if (i*e) % toc == 1:
                return i
            i += 1

    def generate_cipher_manually(self):
        e = int(input('Type public key:'))
        n = int(input('Type n value'))
        self.generate_cipher(e, n)

    def generate_cipher_en(self, e, n):
        s = n + 1
        while s > n:
            s = int(input('Type numeric cipher(lower than n)'))
        v = s ** e % n
        print('Cypher:' + str(v))
        return v


    def generate_cipher(self, uid):
        e, n = self.databasemanager.get_record(uid)
        if not (e is None or n is None):
            self.generate_cipher_en(e, n)

    def decrypt_cipher(self):
        n = int(input('Type your n value:'))
        p = int(input('Type your private key:'))
        cypher = int(input('Type cypher:'))
        v = cypher**p % n
        print('Cypher:'+str(cypher))
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
                #try:
                uid = int(input("Type user Id"))
                self.generate_cipher(uid)
                #except TypeError:
                    #self.generate_cipher()
                return 5
            case '6':
                self.decrypt_cipher()
                return 6
            case '0':
                return 0
