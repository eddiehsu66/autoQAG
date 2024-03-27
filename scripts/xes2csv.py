from pm4py.objects.conversion.log import converter as xes_converter
from pm4py.objects.log.importer.xes import importer as xes_importer

def xes2cev(fromPath:str,toPath:str):

    # 从XES文件中导入日志
    log = xes_importer.apply(fromPath)

    # 将日志转换为数据框
    pd = xes_converter.apply(log, variant=xes_converter.Variants.TO_DATA_FRAME)
    pd.to_csv(toPath, index=False)
if __name__ == '__main__':
    path = r'C:\code\TempHub\pythonp\autoQAG\data\BPI_Challenge_dataset\BPI Challenge 2017.xes'
    outpath = r'C:\code\TempHub\pythonp\autoQAG\data\BPI_Challenge_dataset\BPI Challenge 2017.csv'
    xes2cev(path,outpath)