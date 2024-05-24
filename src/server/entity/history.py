import jsonpickle

from src.config.redisKit import redisInit


class History:
    def __init__(self, uuid):
        self.uuid = uuid
        self.info = ''
        self.chatHistory = []


class Message:
    def __init__(self, id, text, isMine, author):
        self.id = id
        self.text: text
        self.isMine: isMine
        self.author: author


def store_new_history(uuid: str) -> None:
    history = History(uuid)
    try:
        client = redisInit()
        client.set("demoHistory:" + uuid, jsonpickle.encode(history))
    except Exception as e:
        print(f"Exception: {e}")


def get_all_history_keys():
    client = redisInit()
    return client.keys("demoHistory:*")


def get_history_by_uuid(uuid) -> History:
    try:
        client = redisInit()
        data = client.get("demoHistory:" + uuid)
        if data is None:
            return History(uuid)
        return jsonpickle.decode(data)
    except Exception as e:
        print(f"Error: {e}")
        return History(uuid)


def get_chatHistoy_by_uuid(uuid) -> list:
    return get_history_by_uuid(uuid).chatHistory


def add_message(uuid: str, id: int, text: str, isMine: bool, author: str) -> None:
    history = get_history_by_uuid(uuid)
    history.chatHistory.append({
        'id': id,
        'text': text,
        'isMine': isMine,
        'author': author,
    })
    try:
        client = redisInit()
        client.set("demoHistory:" + uuid, jsonpickle.encode(history))
    except Exception as e:
        print(f"Exception: {e}")


if __name__ == '__main__':
    store_new_history('test2')
    add_message('test2', 2, 'hello', True, 'me')
