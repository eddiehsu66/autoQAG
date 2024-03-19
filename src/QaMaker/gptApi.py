import os
from src.QaMaker.configLoad import load_config
from langchain.chat_models import ChatOpenAI
from src.QaMaker.util import tidy
from langchain.schema import (
    AIMessage,  # 等价于OpenAI接口中的assistant role
    HumanMessage,  # 等价于OpenAI接口中的user role
    SystemMessage  # 等价于OpenAI接口中的system role
)


class gptApi:
    """
        api调用封装类
    """

    def __init__(self):
        os.environ["OPENAI_API_KEY"] = load_config("OPENAI_API_KEY")
        os.environ["OPENAI_API_BASE"] = load_config("OPENAI_API_BASE")
        self.llm = ChatOpenAI(temperature=0)
        self.cache = {}

    def get_from_cache(self, query: str):
        """
        从缓存中取回答
        :param query:
        :return:
        """
        hash_code = hash(query)
        return self.cache.get(hash_code)

    def query2llm(self, query: str):
        """
        直接与大模型进行对话
        :param query:
        :return:
        """
        return self.llm.predict(query)

    def prompt2llm(self, prompt: str, query: str, llm=None):
        if llm is None:
            llm = self.llm
        messages = [
            SystemMessage(content=tidy(prompt)),
            HumanMessage(content=tidy(query))
        ]
        ans = llm.predict_messages(messages).content
        self.cache[hash(query)] = ans
        return ans


if __name__ == '__main__':
    gptApi = gptApi()
    print(gptApi.query2llm("一个测试"))
