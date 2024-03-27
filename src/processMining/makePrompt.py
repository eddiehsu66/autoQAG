from src.QaMaker.configLoad import load_config
from scripts.dataFrame import strList2String


def makePrompt(path: str, currentContext: str, predecessorList: str, successorList: str) -> str:
    base = load_config("BASE_PROMPT")
    predecessorContext = strList2String(path, predecessorList)
    successorContext = strList2String(path, successorList)
    contextPrompt = (base + '\n'
                     + f"当前流程日志内容为： {currentContext}" + '\n'
                     + f"上一个流程日志内容为：{predecessorContext}" + '\n'
                     + f"下一个流程日志内容为：{successorContext}")
    return contextPrompt

if __name__ == "__main__":
    makePrompt(r'C:\code\TempHub\pythonp\autoQAG\data\loghub-master\Test\Test_2k.process_add.csv',r"zz"
               ,"['registerCallback not in UI.']","['<*>: Must execute in UI']")