import redis
from src.config.configLoad import load_config


def redisInit():
    pool = redis.ConnectionPool(host=load_config('Redis')['host'], port=load_config('Redis')['port'],
                                decode_responses=True)
    return redis.Redis(connection_pool=pool)

if __name__ == '__main__':
    client = redisInit()
    print(client.get('test'))