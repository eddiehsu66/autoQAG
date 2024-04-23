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


# def dataRate():
#     directory_path = r"C:\code\src\python\autoQAG\data\ipre_data\train\category"
#     file_line_counts = {}
#     for filename in brother:
#         file_path = os.path.join(directory_path, filename + '.txt')
#         if os.path.isfile(file_path):
#             with open(file_path, 'r', encoding='utf-8') as file:
#                 lines = file.readlines()
#                 file_line_counts[filename] = len(lines)
#
#     print(file_line_counts)


def not_in_list(temp: list, num: int):
    directory_path = r"C:\code\src\python\autoQAG\data\ipre_data\train\category"
    num_per_file = num // (34 - len(temp))
    df_list = []
    for file in os.listdir(directory_path):
        filename = file.split('.')[0]
        if filename not in temp:
            df = pd.read_csv(os.path.join(directory_path, file), sep='\t', header=None)
            if len(df) > num_per_file:
                sampled_df = df.sample(n=num_per_file)
            else:
                sampled_df = df
            df_list.append(sampled_df)
    result_df = pd.concat(df_list, ignore_index=True)
    return result_df


def make_train_dataSet(temp: list,num:int):
    directory_path = r"C:\code\src\python\autoQAG\data\ipre_data\train\category"

    max_rows_per_file = num // len(temp)
    new_df = pd.DataFrame()
    for filename in temp:
        pf = pd.read_csv(os.path.join(directory_path, filename + '.txt'), sep='\t', header=None)
        if len(pf) < max_rows_per_file:
            new_df = pd.concat([new_df, pf], ignore_index=True)
        else:
            sampled_pf = pf.sample(n=int(max_rows_per_file))
            new_df = pd.concat([new_df, sampled_pf], ignore_index=True)
    return new_df


def make_train(): # 300/4
    # 其后为测试集的分布
    couple = ['1', '2', '3', '4', '5', '6']  # {'1': 536, '2': 12, '3': 13, '4': 296, '5': 3, '6': 10}
    # 训练集分布
    # {'1': 8142, '2': 218, '3': 183, '4': 5544, '5': 245, '6': 69}
    teacher = ['33', '34']  # {'33': 201, '34': 11}
    # {'33': 2911, '34': 547}
    brother = ['16', '17', '18', '19']  # {'16': 43, '17': 39, '18': 9, '19': 23}
    # {'16': 1673, '17': 637, '18': 532, '19': 805}

    num = 75
    new_df = pd.DataFrame()
    new_df = pd.concat([new_df, make_train_dataSet(couple, num)], ignore_index=True)
    new_df = pd.concat([new_df, make_train_dataSet(teacher, num)], ignore_index=True)
    new_df = pd.concat([new_df, make_train_dataSet(brother, num)], ignore_index=True)
    new_df = pd.concat([new_df, not_in_list(couple + teacher + brother, num)], ignore_index=True)
    new_df.to_csv(r"C:\code\src\python\autoQAG\data\ipre_data\train\train.csv", sep=',', header=False, index=False)


if __name__ == '__main__':
    # pre_process()
    # distribute()
    # get_train_dataSet()
    # dataRate()
    make_train()
