import secrets
import string
import timeit

from rocksdict import Rdict

path = r'C:\code\src\python\autoQAG\cache'


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

    def generate_random_string(length):
        characters = string.ascii_letters + string.digits  # 使用字母和数字生成随机字符串
        return ''.join(secrets.choice(characters) for _ in range(length))


    def test_code():
        db.set(generate_random_string(5), generate_random_string(10))
        print(generate_random_string(5))


    n = 10000
    total_time = timeit.timeit("test_code()", setup="from __main__ import test_code", number=n)
    print(f"Total time to run the code {n} times: {total_time} seconds")
