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
        while p * q < ran:
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
        while i < 5 or num < toc:
            if self.nwd(num, toc) == 1:
                i += 1
                tab.append(num)
            num += 1
        return tab[randint(0, 5)]

    def generate_private_key(self, e, toc):
        i = 1
        while True:
            if (i * e) % toc == 1:
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
        v = cypher ** p % n
        print('Cypher:' + str(cypher))
        print('Decrypted cypher:' + str(v))
        return v

    def add_user(self, uid, nick, p, n):
        self.databasemanager.insert_record(uid, nick, p, n)

    def delete_user(self, idd):
        self.databasemanager.delete_record(idd)

    def print_database(self):
        self.databasemanager.print_all()

