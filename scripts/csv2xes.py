from pm4py.objects.conversion.log import converter as xes_converter
from pm4py.objects.log.importer.xes import importer as xes_importer
import pandas as pd
import pm4py


def csv2xes(fromPath: str, toPath: str):
    # 从CSV文件中导入数据框
    dataframe = pd.read_csv(fromPath)
    dataframe['Time'] = pd.to_datetime(dataframe['Time'], format='%H:%M:%S.%f')

    # 格式化数据框以符合pm4py的要求
    dataframe = pm4py.format_dataframe(dataframe, case_id='Component', activity_key='EventTemplate',
                                       timestamp_key='Time',timest_format='%H:%M:%S.%f')

    # 将数据框转换为事件日志对象
    event_log = pm4py.convert_to_event_log(dataframe)

    # 将事件日志对象写入XES文件
    pm4py.write_xes(event_log, toPath)


if __name__ == '__main__':
    path = r'C:\code\TempHub\pythonp\autoQAG\data\loghub-master\Test\Test_2k.log_structured.csv'
    outpath = r'C:\code\TempHub\pythonp\autoQAG\data\loghub-master\Test\Test_2k.log_structured.xes'
    csv2xes(path, outpath)
