import io
import os

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
        key_df = sent_train.loc[value, [1, 2, 3]].copy()
        key_df[4] = 'NAN' if key == "0" else relation_map.get(key, 'NAN')
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
    sent_train.to_csv(r"C:\code\src\python\autoQAG\data\ipre_data\train\merged_sent_train.csv", sep=',', header=False,
                      index=False)


def get_train_dataSet():
    directory_path = r"C:\code\src\python\autoQAG\data\ipre_data\train\category"

    # 初始化一个空的DataFrame用于存储所有抽取的样本
    all_samples = pd.DataFrame()

    # 遍历指定目录下的所有CSV文件
    for filename in os.listdir(directory_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory_path, filename)

            # 读取CSV文件
            df = pd.read_csv(file_path, sep='\t', header=None)
            num_samples = len(df)

            # 如果样本数少于50，则抽取全部样本；否则，随机抽取50个样本
            if num_samples <= 30:
                samples = df
            else:
                samples = df.sample(n=30)
            all_samples = pd.concat([all_samples, samples], ignore_index=True)
    out_path = r"C:\code\src\python\autoQAG\data\ipre_data\train\ipre_train.csv"
    all_samples.to_csv(out_path, index=False, header=False)


if __name__ == '__main__':
    # pre_process()
    # distribute()
    get_train_dataSet()
