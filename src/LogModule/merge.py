import pandas as pd
import sys

sys.path.append('/src/QaMaker')
from src.QaMaker.configLoad import load_config


def mergeLog(filename: str):
    # 读取CSV文件
    df = pd.read_csv(f'../../data/loghub-master/{filename}/{filename}_2k.log_structured.csv')
    # 通过将相邻重复的eventId属性进行分组，然后对每个组执行合并操作
    df['group'] = (df['EventId'] != df['EventId'].shift()).cumsum()

    agg_columns = ['LineId', 'Content', 'EventId', 'EventTemplate']
    result_df = df.groupby(['EventId', 'group'], as_index=False)[agg_columns].agg({
        'LineId': 'first',
        'Content': ','.join,
        'EventId': 'first',
        'EventTemplate': ','.join,
    })

    # 删除用于分组的辅助列
    result_df.drop('group', axis=1, inplace=True)
    result_df.sort_values(by='LineId', ascending=True, inplace=True)

    # 将结果保存到新的CSV文件
    result_df.to_csv(f'../../data/loghub-master/{filename}/{filename}_2k.merged_file.csv', index=False)


def getFold() -> []:
    foldList = load_config("DATA_LIST").split(',')
    return foldList


def mergeAll():
    foldList = getFold()
    for filename in foldList:
        mergeLog(filename)


if __name__ == '__main__':
    mergeAll()
