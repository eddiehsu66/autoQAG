import os

import pandas as pd
from logparser.Drain import LogParser
from src.config.configLoad import load_config,find_nearest_dir
from src.evaluation.accuracy import evaluate_test

def logParse(fileName:str):
    base = find_nearest_dir('data')
    dirName = os.path.join(base,rf'loghub-master\{fileName}')
    outName = os.path.join(base,rf'loghub-master\{fileName}\{fileName}_DrainParsed')
    settings = load_config("PARSE_SETTING")
    log_file = settings[fileName]["log_file"]
    parser = LogParser(
        settings[fileName]["log_format"],
        indir=dirName,
        outdir=outName,
        depth=settings[fileName]["depth"],
        st=settings[fileName]["st"],
        rex=settings[fileName]["regex"]
    )
    parser.parse(log_file)

    file1_df = pd.read_csv(dirName + rf"\{fileName}_2k.log_testData.csv")
    file2_df = pd.read_csv(outName + rf"\{fileName}_2k.log_structured.csv")

    result = []
    for index, row in file1_df.iterrows():
        line_id = row['LineId']
        cur_row = []
        # 在file2_df中查找具有相同LineId的行
        matching_row = file2_df[file2_df['LineId'] == line_id]

        # 如果找到匹配的行
        if not matching_row.empty:
            event_template1 = row['EventTemplate']
            event_template2 = matching_row['EventTemplate'].values[0]
            cur_row.append(row['Content'])
            cur_row.append(event_template2)
            cur_row.append("NoPrompt")
            cur_row.append(event_template1)
            result.append(cur_row)
    print(evaluate_test(result))
if __name__ == '__main__':
    data = ["Hadoop","BGL","MAC","HPC"]
    logParse("Hadoop")