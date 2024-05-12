import redis
from src.config.configLoad import load_config


def redisInit():
    pool = redis.ConnectionPool(host=load_config('Redis')['host'], port=load_config('Redis')['port'],
                                decode_responses=True,password = load_config('Redis')['password'])
    return redis.Redis(connection_pool=pool)

if __name__ == '__main__':
    client = redisInit()
    # print(client.set('test', 'test'))
    # # client.flushall()
    print(client.get('test'))
    # client.flushall()