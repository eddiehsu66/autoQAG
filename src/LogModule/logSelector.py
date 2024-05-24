import json
import os
import string

import pandas as pd
import re
from sklearn.utils import shuffle
import textdistance
import random
import heapq
from collections import Counter
import time
import calendar
from src.config.configLoad import load_config


def lcs_distance(x, y):
    seq1 = x.split()
    seq2 = y.split()
    lengths = [[0 for j in range(len(seq2) + 1)] for i in range(len(seq1) + 1)]
    # row 0 and column 0 are initialized to 0 already
    for i in range(len(seq1)):
        for j in range(len(seq2)):
            if seq1[i] == seq2[j]:
                lengths[i + 1][j + 1] = lengths[i][j] + 1
            else:
                lengths[i + 1][j + 1] = max(lengths[i + 1][j], lengths[i][j + 1])

    return 1 - 2 * lengths[-1][-1] / (len(seq1) + len(seq2))


def lev_distance(x, y):
    return textdistance.levenshtein.normalized_distance(x, y)


def euc_distance(x, y):
    return textdistance.cosine.normalized_distance(x, y)


def jaccard_distance(x, y):
    return textdistance.jaccard.normalized_distance(x.split(), y.split())


def ratcliff_distance(x, y):
    return textdistance.ratcliff_obershelp.normalized_distance(x, y)


def min_distance(c_set, t_set):
    D = []
    for c_inst in c_set:
        min_candidate_distance = 1e10
        for t_inst in t_set:
            min_candidate_distance = min(min_candidate_distance, jaccard_distance(c_inst, t_inst))
        D.append(min_candidate_distance)
    return D


def adaptive_random_sampling(logs, k, n_candidate=128):
    sample_set = []
    T = []
    for r in range(k):
        print("r: ", r)
        if len(sample_set) == 0:
            i = max(range(0, len(logs)), key=lambda x: (len(logs[x][0].split()), logs[x][2]))
            T.append(logs[i][0])
            sample_set.append(logs[i][1])
            # del logs[i]
            continue
        candidate_set = [(x, logs[x]) for x in range(len(logs)) if x in random.sample(range(len(logs)), n_candidate)]
        candidate_set = sorted(candidate_set, key=lambda x: x[1][2], reverse=True)
        candidate_distance = min_distance([x[1][0] for x in candidate_set], T)
        best_candidate = max(range(len(candidate_distance)), key=candidate_distance.__getitem__)
        T.append(candidate_set[best_candidate][1][0])
        sample_set.append(candidate_set[best_candidate][1][1])
        # del logs[candidate_set[best_candidate][0]]
    return sample_set


# shot * (candidate + candidate*log_candidate, candidate * shot * distance)


class Vocab:
    def __init__(self, stopwords=["<*>"]):
        stopwords = [
                        "a",
                        "an",
                        "and",
                        "i",
                        "ie",
                        "so",
                        "to",
                        "the",

                    ] + list(calendar.day_name) + list(calendar.day_abbr) \
                    + list(calendar.month_name) + list(calendar.month_abbr)
        self.token_counter = Counter()
        self.stopwords = frozenset(set(stopwords))
        # print(self.__filter_stopwords(['LDAP', 'Built', 'with']))

    def build(self, sequences):
        # print("Build vocab with examples: ", len(sequences))
        for sequence in sequences:
            sequence = self.__filter_stopwords(sequence)
            # print(sequence)
            self.update(sequence)

    def update(self, sequence):
        sequence = self.__filter_stopwords(sequence)
        self.token_counter.update(sequence)

    def topk_tokens(self, sequence, topk=3):
        sequence = self.__filter_stopwords(sequence)
        token_count = [(token, self.token_counter[token]) for token in set(sequence)]
        topk_tuples = heapq.nlargest(topk, token_count, key=lambda x: x[1])
        topk_keys = tuple([t[0] for t in topk_tuples])
        return topk_keys

    def __len__(self):
        return len(self.token_counter)

    def __filter_stopwords(self, sequence):
        return [
            token
            for token in sequence
            if (len(token) > 2) and (token not in self.stopwords)
        ]


def clean(s):
    log_format = re.sub(r'[0-9A-Za-z, ]+', '', s)
    unique_chars = list(set(log_format))
    sorted_string = ''.join(sorted(unique_chars))
    s = re.sub(':|\(|\)|=|,|"|\{|\}|@|$|\[|\]|\||;|\.?!', ' ', s)
    s = " ".join([word for word in s.strip().split() if not bool(re.search(r'\d', word))])
    # trantab = str.maketrans(dict.fromkeys(list(string.punctuation)))
    return s, sorted_string


def hierichical_clustering(contents):
    t1 = time.time()
    vocab = Vocab()
    vocab.build([v[0].split() for v in contents.values()])
    t2 = time.time()
    # print("Build time: ", t2 - t1)

    # hierichical clustering
    hierichical_clusters = {}
    for k, v in contents.items():
        frequent_token = tuple(sorted(vocab.topk_tokens(v[0].split(), 3)))
        log_format = v[1]
        if frequent_token not in hierichical_clusters:
            hierichical_clusters[frequent_token] = {"size": 1, "cluster": {log_format: [k]}}
        else:
            hierichical_clusters[frequent_token]["size"] = hierichical_clusters[frequent_token]["size"] + 1
            if log_format not in hierichical_clusters[frequent_token]["cluster"]:
                hierichical_clusters[frequent_token]["cluster"][log_format] = [k]
            else:
                hierichical_clusters[frequent_token]["cluster"][log_format].append(k)
    # print("Number of coarse-grained clusters: ", len(hierichical_clusters.keys()))
    total_fine_clusters = 0
    for k, v in hierichical_clusters.items():
        total_fine_clusters += len(hierichical_clusters[k]["cluster"])
    # print("Number of fine-grained clusters: ", total_fine_clusters)
    return hierichical_clusters


def hierichical_distribute(hierichical_clusters, shot, labelled_logs=[]):
    # hierichical distribution
    candidate_samples = []
    coarse_clusters = hierichical_clusters.keys()
    coarse_clusters = shuffle(list(coarse_clusters))
    # coarse_clusters = sorted(coarse_clusters, key=lambda x: hierichical_clusters[x]["size"], reverse=True)
    corase_size = len(coarse_clusters)
    for coarse_id, coarse_key in enumerate(coarse_clusters):
        coarse_quota = int(shot // corase_size) + (coarse_id < shot % corase_size)
        if coarse_quota == 0:
            break
        # print("Coarse quota: ", coarse_quota)
        # coarse cluster of coarse_key has been allocated {coarse_quota}
        fine_clusters = hierichical_clusters[coarse_key]["cluster"].keys()
        fine_clusters = sorted(fine_clusters, key=lambda x: len(hierichical_clusters[coarse_key]["cluster"][x]),
                               reverse=True)
        fine_size = len(fine_clusters)
        # print("Fine size: ", fine_size)
        for fine_id, fine_key in enumerate(fine_clusters):
            fine_quota = int(coarse_quota // fine_size) + (fine_id < coarse_quota % fine_size)
            if fine_quota == 0:
                break
            # print("Fine quota: ", fine_quota)
            # fine cluster of fine_key has been allocated {fine_quota}
            # print("Coarse key: ", coarse_key, " Fine key: ", fine_key, " Fine quota: ", fine_quota, " Corase quota: " , coarse_quota, len(hierichical_clusters[coarse_key]["cluster"][fine_key]))
            samples = random.choices(hierichical_clusters[coarse_key]["cluster"][fine_key], k=fine_quota)
            candidate_samples.extend(samples)

    return candidate_samples


def candidateSample(category, shotNum, mode="others"):
    path = rf'../../cache/loghub/{category}'

    log_file = load_config("PARSE_SETTING")[category]["log_file"]

    if mode == "sampled":
        labelled_logs = pd.read_csv(f'{path}/{log_file}_trainData.csv')
    else:
        labelled_logs = pd.read_csv(f'{path}/{log_file}_structured.csv')

    k_rate = 1
    length = int(k_rate * len(labelled_logs))
    labelled_logs = labelled_logs[:length]
    # labelled_logs = labelled_logs[:length].drop_duplicates(['Content'], keep='first')
    # print("Removed length: ", len(labelled_logs))
    # train_df = labelled_logs.sample(n=2000)
    contents = {}
    for i, x in enumerate(labelled_logs['Content'].to_list()):
        x, fx = clean(x)
        if len(x.split()) > 1:
            contents[i] = (x, fx)
    # content = {i: clean(x) if len(x.split()) > 1 for i, x in enumerate(labelled_logs['Content'].tolist())}

    hierichical_clusters = hierichical_clustering(contents)

    shot = shotNum

    sampled_ids = hierichical_distribute(hierichical_clusters, shot, labelled_logs['Content'].to_list())

    sampled_data = labelled_logs.take(sampled_ids)
    remaining_data = labelled_logs.drop(sampled_ids)

    # 打开文件准备写入
    # if mode == "sampled":
    #     sampled_data_outpath = f"{path}/{category}_2k.log_32sampled.csv"
    #     remaining_data_outpath = f"{path}/{category}_2k.log_remainingSampled.csv"
    #     sampled_data.to_csv(sampled_data_outpath, index=False, encoding='utf-8')
    #     remaining_data.to_csv(remaining_data_outpath, index=False, encoding='utf-8')
    # else:
    #     outpath = f"{path}/{category}_2k.log_sampled.csv"
    #     sampled_data.to_csv(outpath, index=False, encoding='utf-8')
    return sampled_data


def random_select_log(num, category):
    path = rf'../../cache/loghub/{category}'
    df = pd.read_csv(path + rf'\{category}_2k.log_sampledFile.csv', encoding='utf-8')

    # 随机抽取num个行
    train_indices = sorted(random.sample(range(len(df)), num))
    train_df = df.iloc[train_indices]

    # 获取剩余的行
    test_df = df.drop(train_indices)

    # 分别保存到train_input, train_output, test_input, test_output
    # train_input = train_df.drop(columns=['Content'])
    # train_output = train_df['EventTemplate']
    # test_input = test_df.drop(columns=['Content'])
    # test_output = test_df['EventTemplate']
    train_df.to_csv(path + rf'\{category}_2k.log_trainData.csv', index=False, encoding='utf-8')
    test_df.to_csv(path + rf'\{category}_2k.log_testData.csv', index=False, encoding='utf-8')
    # return train_input, train_output, test_input, test_output


def select_log(category, order, shotNum) -> (list, list, list, list):
    data_dir = f"../../cache/loghub/{category}"
    if not os.path.exists(f"{data_dir}/process"):
        os.makedirs(f"{data_dir}/process")

    log_file = load_config("PARSE_SETTING")[category]["log_file"]

    labelled_logs = pd.read_csv(f'{data_dir}/{log_file}_sampledFile.csv')

    k_rate = 1
    length = int(k_rate * len(labelled_logs))
    labelled_logs = labelled_logs[:length]

    contents = {}
    for i, x in enumerate(labelled_logs['Content'].to_list()):
        x, fx = clean(x)
        if len(x.split()) > 1:
            contents[i] = (x, fx)

    hierichical_clusters = hierichical_clustering(contents)

    shot = shotNum

    sampled_ids = hierichical_distribute(hierichical_clusters, shot, labelled_logs['Content'].to_list())

    candidate_samples = [(row['Content'], row['EventTemplate']) for _, row in
                         labelled_logs.take(sampled_ids).iterrows()]
    candidate_samples = [{"query": x[0], "answer": x[1]} for x in
                         candidate_samples]
    with open(f"{data_dir}/process/{shot}shot{order}.json", "w") as f:
        for s in candidate_samples[:shot]:
            f.write(json.dumps(s) + "\n")

    queries = [sample["query"] for sample in candidate_samples]
    answers = [sample["answer"] for sample in candidate_samples]

    # 获取剩余的数据
    remaining_data = labelled_logs.drop(sampled_ids)
    remaining_samples = [(row['Content'], row['EventTemplate']) for _, row in remaining_data.iterrows()]
    remaining_samples = [{"query": x[0], "answer": x[1]} for x in remaining_samples]

    remaining_queries = [sample["query"] for sample in remaining_samples]
    remaining_answers = [sample["answer"] for sample in remaining_samples]

    return queries, answers, remaining_queries, remaining_answers


def get_train_log(fileName: str) -> (list, list):
    data_dir = f"C:/code/src/python/autoQAG/data/loghub-master/{fileName}"
    log_file = load_config("PARSE_SETTING")[f"{fileName}"]["log_file"]
    labelled_logs = pd.read_csv(f'{data_dir}/{log_file}_remainingSampled.csv')

    content_list = labelled_logs['Content'].tolist()
    template_list = labelled_logs['EventTemplate'].tolist()

    # 返回两个列表
    return content_list, template_list


def get_test_log(fileName: str) -> (list, list):
    data_dir = f"C:/code/src/python/autoQAG/data/loghub-master/{fileName}"
    log_file = load_config("PARSE_SETTING")[f"{fileName}"]["log_file"]
    labelled_logs = pd.read_csv(f'{data_dir}/{log_file}_testData.csv')

    content_list = labelled_logs['Content'].tolist()
    template_list = labelled_logs['EventTemplate'].tolist()

    # 返回两个列表
    return content_list, template_list


def get_random_log(num, fileName) -> (list, list):
    data_dir = f"C:/code/src/python/autoQAG/data/loghub-master/{fileName}"
    df = pd.read_csv(data_dir + rf'\{fileName}_2k.log_32sampled.csv', encoding='utf-8')
    # 随机抽取num个行
    indices = sorted(random.sample(range(len(df)), num))
    df = df.iloc[indices]

    content_list = df['Content'].tolist()
    template_list = df['EventTemplate'].tolist()
    return content_list, template_list


def select_clean(s):
    s = re.sub(':|\(|\)|=|,|"|\{|\}|@|$|\[|\]|\||;|\.', ' ', s)
    s = " ".join([word.lower() if word.isupper() else word for word in s.strip().split()])
    s = re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', s))
    s = " ".join([word for word in s.split() if not bool(re.search(r'\d', word))])
    trantab = str.maketrans(dict.fromkeys(list(string.punctuation)))
    s = s.translate(trantab)
    s = " ".join([word.lower().strip() for word in s.strip().split()])
    return s


def prompt_select(log, k, sampled_file):
    if k == 0:
        return []
    df = sampled_file
    examples = []
    L = df.to_dict('records')
    log = select_clean(log)
    for d in L:
        d['similarity'] = jaccard_distance(select_clean(d['Content']), log)
    sorted_dicts = sorted(L, key=lambda d: d['similarity'], reverse=False)
    result = sorted_dicts[:k]

    for x in result:
        examples.append({'Content': f"{x['Content']}",
                         'answer': f"{x['EventTemplate']}"})
    return examples


def select_candidateSampleLog(category: str, uuid:str,log_content:str,shotNum: int):
    sampled_path = f'../../cache/logs/{uuid}/Test_sampled.csv'
    if not os.path.exists(sampled_path):
        sampled_file = candidateSample(category, shotNum, 'others')
    else:
        sampled_file = pd.read_csv(sampled_path)
    return prompt_select(log_content, 5, sampled_file)


if __name__ == '__main__':
    select_candidateSampleLog('Test', 'test',128)
