import os

from src.QaMaker.gptApi import gptApi
from src.config.configLoad import load_config
from src.QaMaker.util import extractQA


class QaServer:
    def __init__(self,prompt=''):
        self.agent = gptApi()
        self.prompt = prompt

    def genQaBot(self) -> object:
        if self.prompt == '':
            self.prompt = \
                f""" 您是一个问答对生成器。
                        我之后会提供相关的文本片段或对话记录。
                        您需要生成一个问题和相应的答案，并确保问题和答案都基于上下文。
                        如果无法生成问题，请回复“当前语句段无法生成问题。”
                        在回答中不要包含过于个人化的内容。
                        请记住，您只能根据提供的内容来生成问题与答案。
                        必须使用{"Chinese"}进行回应。
                        """
        os.environ["OPENAI_API_KEY"] = load_config("OPENAI_API_KEY")
        os.environ["OPENAI_API_BASE"] = load_config("OPENAI_API_BASE")
        self.agent = gptApi()
        return self

    def reset(self):
        return self.genQaBot()

    def getQuestAnsPair(self, text: str):
        if self.agent is None:
            self.agent = gptApi()
        qap = self.agent.prompt2llm(self.prompt, text)
        # lifeTime = 4
        # while qap[0] and lifeTime >4:
        #     qap = self.agent.prompt2llm(self.prompt,text)
        #     lifeTime = lifeTime - 1
        return extractQA(qap)


if __name__ == "__main__":
    app = QaServer().genQaBot()
    print(app.getQuestAnsPair("[2024-03-07 10:15:30] 用户123登录成功"))
