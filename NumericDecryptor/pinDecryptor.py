import math
from random import randint
from databaseManager import DatabaseManager


class PinDecryptor:
    def __init__(self):
        self.databasemanager = DatabaseManager()
        self.public_key = None
        self.cypher_range = None
        self.init_id()

    def init_id(self):
        try:
            with open('myid.txt', 'r') as f:
                lines = f.readlines()
                count = sum(1 for line in lines)
                if count == 2:
                    self.public_key = lines[0].rsplit()[0]
                    self.cypher_range = lines[1]
        except FileNotFoundError:
            self.public_key = 'xxx'
            self.cypher_range = 'xxxx'

    def update_id(self, public_key, cypher_range):
        self.public_key = public_key
        self.cypher_range = cypher_range
        f = open('myid.txt', 'w')
        f.writelines('{0}\n{1}'.format(public_key, cypher_range))
        f.close()

    def generate_identity(self, cypher_range):
        cypher_range = int(cypher_range)
        n, t = DecryptorMath.initialize_range_and_tocjent(cypher_range)
        pub = DecryptorMath.generate_public_key(t)
        priv = DecryptorMath.generate_private_key(pub, t)
        self.update_id(pub, n)
        return pub, priv, n

    def add_user(self, uid, nick, p, n):
        self.databasemanager.insert_record(uid, nick, p, n)

    def delete_user(self, idd):
        self.databasemanager.delete_record(idd)

    def get_data(self):
        return [self.public_key, self.cypher_range]


class DecryptorMath:
    @staticmethod
    def is_prime(value):
        max_check = math.ceil(math.sqrt(value))
        for i in range(max_check):
            if i > 1 and value % i == 0:
                return False
        return True

    @staticmethod
    def nwd(a, b):
        while a != b:
            if a > b:
                a -= b
            else:
                b -= a
        return a

    @staticmethod
    def generate_public_key(tocjent):
        i = 0
        num = 2
        tab = []
        _range = 50
        while not (i > _range or num > tocjent):
            if num % 2 == 1 and DecryptorMath.nwd(num, tocjent) == 1:
                i += 1
                tab.append(num)
            num += 1
        return tab[randint(0, len(tab))]

    @staticmethod
    def generate_private_key(pub_key, tocjent):
        i = 1
        while True:
            if (i * pub_key) % tocjent == 1:
                return i
            i += 1

    @staticmethod
    def initialize_range_and_tocjent(key_range):
        n = t = 0
        are_prime = False
        while not are_prime:
            p = DecryptorMath.generate_prime(321)  # 321 ensure enough range for pin
            q = DecryptorMath.generate_prime(321)
            if p*q > key_range:
                n = p * q  # range
                t = (p - 1) * (q - 1)  # tocjent
                are_prime = True
        return n, t

    @staticmethod
    def generate_prime(_range: int):
        v = randint(2, _range)
        while not DecryptorMath.is_prime(v):
            v = randint(2, _range)
        return v

    @staticmethod
    def encrypt_cypher(_pub_key, _range, _cipher):
        try:
            _pub_key = int(_pub_key)
            _cipher = int(_cipher)
            _range = int(_range)
            condition = _cipher < _range
            if condition:
                return _cipher ** _pub_key % _range
            else:
                return 'Cipher cannot be higher than Range'
        except ValueError:
            return 'Some value is not an Integer'

    @staticmethod
    def decrypt_cipher(cypher, _range, priv_key):
        cypher = int(cypher)
        priv_key = int(priv_key)
        _range = int(_range)
        v = cypher ** priv_key % _range# use pubkey instead of range if bugs
        return v
