import secrets
import string
import timeit

from rocksdict import Rdict

path = r'../../cache/rocksdb'


class RocksDB:
    def __init__(self, path=path):
        self.db = Rdict(path)
        self.path = path

    def set(self, key, value):
        self.db[key] = value

    def get(self, key):
        return self.db[key]

    def del_all(self):
        self.db.close()
        Rdict.destroy(self.path)

    def __exit__(self):
        self.db.close()


if __name__ == '__main__':
    db = RocksDB()

    db.set("test","item1")
    db.__exit__()
    b = RocksDB()
    print(b.get("test"))
