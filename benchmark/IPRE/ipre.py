import io

import pandas as pd


def distribute():
    relation2id = pd.read_csv(r"C:\code\src\python\autoQAG\data\ipre_data\relation2id.txt", sep='\t', header=None)
    relation_dict = {}
    relation_map = {}

    for index, row in relation2id.iterrows():
        key = str(row[1])
        relation_map[key] = row[0]
        relation_dict[key] = []

    sent_relation_train = pd.read_csv(r"C:\code\src\python\autoQAG\data\ipre_data\train\sent_relation_train.txt",
                                      sep='\t', header=None)
    for index, row in sent_relation_train.iterrows():
        for i in str(row[1]).split(' '):
            relation_dict[i].append(row[0])

    sent_train = pd.read_csv(r"C:\code\src\python\autoQAG\data\ipre_data\train\merged_sent_train.csv", sep=',',
                               header=None)
    sent_train.set_index(0, inplace=True)
    outFile = r"C:\code\src\python\autoQAG\data\ipre_data\train\category"
    for key, value in relation_dict.items():
        key_df = sent_train.loc[value,[1,2,3]].copy()
        key_df[4] = 'NA' if key == "0" else relation_map.get(key, 'NA')
        key_df.to_csv(outFile + r"\\" + str(key) + ".txt", sep='\t', header=False, index=False)
        print(f"{key}轮结束")


def pre_process():
    with open(r"C:\code\src\python\autoQAG\data\ipre_data\train\sent_train_1.txt", "r",
              encoding="utf-8") as original_file:
        content = original_file.read()
    content = content.replace('" ', "")
    with open(r"C:\code\src\python\autoQAG\data\ipre_data\train\processed_sent_train_1.txt", "w",
              encoding="utf-8") as processed_file:
        processed_file.write(content)
        
    with open(r"C:\code\src\python\autoQAG\data\ipre_data\train\sent_train_2.txt", "r",
              encoding="utf-8") as original_file:
        content = original_file.read()
    content = content.replace('" ', "")
    with open(r"C:\code\src\python\autoQAG\data\ipre_data\train\processed_sent_train_2.txt", "w",
              encoding="utf-8") as processed_file:
        processed_file.write(content)
        
    sent_train_1 = pd.read_csv(r"C:\code\src\python\autoQAG\data\ipre_data\train\processed_sent_train_1.txt", sep='\t',
                               header=None)
    sent_train_2 = pd.read_csv(r"C:\code\src\python\autoQAG\data\ipre_data\train\processed_sent_train_2.txt", sep='\t',
                               header=None)

    sent_train = pd.concat([sent_train_1, sent_train_2])
    sent_train.to_csv(r"C:\code\src\python\autoQAG\data\ipre_data\train\merged_sent_train.csv", sep=',', header=False, index=False)

if __name__ == '__main__':
    pre_process()
    distribute()
    # pd.set_option('display.max_columns', None)
    # pd.set_option('display.max_rows', None)
    # sent_train_2 = pre_process()
    # print(sent_train_2.head(11369))
