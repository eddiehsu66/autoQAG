import pandas as pd


def getByColumnName(path: str, eventTemplate: str, columnName: str,contentList:list):
    # 使用pandas读取CSV文件
    df = pd.read_csv(path)
    # 检查列名是否存在于DataFrame中
    if columnName in df.columns:
        rows = df[df['EventTemplate'] == eventTemplate]
        for index,row in rows.iterrows():
            contentList.append(str(row[columnName]))


def strList2String(path: str, strList: str) -> str:
    ids = eval(strList)
    if len(ids) == 0:
        return ""
    contentList = list()
    for id in ids:
        getByColumnName(path, str(id), 'Content',contentList)
    return '\n'.join(contentList)

def covertListToDataFrame(extracted_data, columnsName):
    df = pd.DataFrame(extracted_data, columns=[columnsName])
    return df

if __name__ == '__main__':
    print(strList2String(r'C:\code\TempHub\pythonp\autoQAG\data\loghub-master\Test\Test_2k.log_structured.csv',
                         strList="['<*>: Must execute in UI', '*** unregister callback for null']"))
