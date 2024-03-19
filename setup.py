from src.LogModule.logParse import logParse
from src.LogModule.merge import mergeLog
from src.LogModule.log2QA import log2QA


def logToQA(fileName:str):
    logParse(fileName)
    mergeLog(fileName)
    log2QA(fileName)


if __name__ == '__main__':
    logToQA('Test')
