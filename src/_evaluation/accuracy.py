import re
import pandas as pd
from tqdm import tqdm

from src._LogModule.AutoPrompt.promptBranch.extract_log import extract_log_template
from src.config.unitTest import get_test_results
from scripts.dataFrame import covertListToDataFrame


def post_process_tokens(tokens, punc):
    excluded_str = ['=', '|', '(', ')']
    for i in range(len(tokens)):
        if tokens[i].find("<*>") != -1:
            tokens[i] = "<*>"
        else:
            new_str = ""
            for s in tokens[i]:
                if (s not in punc and s != ' ') or s in excluded_str:
                    new_str += s
            tokens[i] = new_str
    return tokens


def message_split(message):
    punc = "!\"#$%&'()+,-/:;=?@.[\]^_`{|}~"
    splitters = "\s\\" + "\\".join(punc)
    splitter_regex = re.compile("([{}]+)".format(splitters))
    tokens = re.split(splitter_regex, message)
    tokens = list(filter(lambda x: x != "", tokens))

    # print("tokens: ", tokens)
    tokens = post_process_tokens(tokens, punc)
    tokens = [
        token.strip()
        for token in tokens
        if token != "" and token != ' '
    ]
    tokens = [
        token
        for idx, token in enumerate(tokens)
        if not (token == "<*>" and idx > 0 and tokens[idx - 1] == "<*>")
    ]
    return tokens


def calculate_similarity(template1, template2):
    template1 = message_split(template1)
    template2 = message_split(template2)
    intersection = len(set(template1).intersection(set(template2)))
    union = (len(template1) + len(template2)) - intersection
    return intersection / union


# 计算TPA
def calculate_parsing_accuracy_template(groundtruth_df, parsedresult_df, filter_templates=None):
    # parsedresult_df = pd.read_csv(parsedresult)
    # groundtruth_df = pd.read_csv(groundtruth)
    if filter_templates is not None:
        groundtruth_df = groundtruth_df[groundtruth_df['EventTemplate'].isin(filter_templates)]
        parsedresult_df = parsedresult_df.loc[groundtruth_df.index]
    correctly_parsed_messages = parsedresult_df[['EventTemplate']].eq(groundtruth_df[['EventTemplate']]).values.sum()
    total_messages = len(parsedresult_df[['Content']])

    PA = float(correctly_parsed_messages) / total_messages

    # similarities = []
    # for index in range(len(groundtruth_df)):
    #     similarities.append(calculate_similarity(groundtruth_df['EventTemplate'][index], parsedresult_df['EventTemplate'][index]))
    # SA = sum(similarities) / len(similarities)
    # print('Parsing_Accuracy (PA): {:.4f}, Similarity_Accuracy (SA): {:.4f}'.format(PA, SA))
    print('Parsing_Accuracy (PA): {:.4f}'.format(PA))
    return PA


# 计算PA
def calculate_pa(groundtruth_df, parsedresult_df):
    groundtruth_templates = list(groundtruth_df['EventTemplate'])
    parsedresult_templates = list(parsedresult_df['EventTemplate'])
    correctly_parsed_messages = 0
    for i in range(len(groundtruth_templates)):
        if correct_lstm(groundtruth_templates[i], parsedresult_templates[i]):
            correctly_parsed_messages += 1

    PA = float(correctly_parsed_messages) / len(groundtruth_templates)

    # similarities = []
    # for index in range(len(groundtruth_df)):
    #     similarities.append(calculate_similarity(groundtruth_df['EventTemplate'][index], parsedresult_df['EventTemplate'][index]))
    # SA = sum(similarities) / len(similarities)
    # print('Parsing_Accuracy (PA): {:.4f}, Similarity_Accuracy (SA): {:.4f}'.format(PA, SA))
    return PA


def correct_lstm(groudtruth, parsedresult):
    tokens1 = groudtruth.split(' ')
    tokens2 = parsedresult.split(' ')
    tokens1 = ["<*>" if "<*>" in token else token for token in tokens1]
    tokens2 = ["<*>" if "<*>" in token else token for token in tokens2]
    return tokens1 == tokens2


# 计算ga和fga

def calculate_ga_fga(df_groundtruth, df_parsedlog):
    null_logids = df_groundtruth[~df_groundtruth['EventTemplate'].isnull()].index
    df_groundtruth = df_groundtruth.loc[null_logids]
    df_parsedlog = df_parsedlog.loc[null_logids]
    (GA, FGA) = get_accuracy(df_groundtruth['EventTemplate'], df_parsedlog['EventTemplate'])
    return GA, FGA


def get_accuracy(series_groundtruth, series_parsedlog, filter_templates=None):
    series_groundtruth_valuecounts = series_groundtruth.value_counts()
    series_parsedlog_valuecounts = series_parsedlog.value_counts()
    df_combined = pd.concat([series_groundtruth, series_parsedlog], axis=1, keys=['groundtruth', 'parsedlog'])
    grouped_df = df_combined.groupby('groundtruth')
    accurate_events = 0  # determine how many lines are correctly parsed
    accurate_templates = 0
    if filter_templates is not None:
        filter_identify_templates = set()
    for ground_truthId, group in grouped_df:
        series_parsedlog_logId_valuecounts = group['parsedlog'].value_counts()
        if filter_templates is not None and ground_truthId in filter_templates:
            for parsed_eventId in series_parsedlog_logId_valuecounts.index:
                filter_identify_templates.add(parsed_eventId)
        if series_parsedlog_logId_valuecounts.size == 1:
            parsed_eventId = series_parsedlog_logId_valuecounts.index[0]
            if len(group) == series_parsedlog[series_parsedlog == parsed_eventId].size:
                if (filter_templates is None) or (ground_truthId in filter_templates):
                    accurate_events += len(group)
                    accurate_templates += 1
    if filter_templates is not None:
        GA = float(accurate_events) / len(series_groundtruth[series_groundtruth.isin(filter_templates)])
        PGA = float(accurate_templates) / len(filter_identify_templates)
        RGA = float(accurate_templates) / len(filter_templates)
    else:
        GA = float(accurate_events) / len(series_groundtruth)
        PGA = float(accurate_templates) / len(series_parsedlog_valuecounts)
        RGA = float(accurate_templates) / len(series_groundtruth_valuecounts)
    # print(FGA, RGA)
    FGA = 0.0
    if PGA != 0 or RGA != 0:
        FGA = 2 * (PGA * RGA) / (PGA + RGA)
    return GA, FGA


def prompt_accuracy_count(prompts, results):
    key_counts = {prompts: 0 for prompts in prompts}
    Accuracy = {prompt: 0 for prompt in prompts}
    for index, item in enumerate(results):
        key_counts[item[2]] = key_counts[prompts] + 1
        if item[1] == item[3]:
            Accuracy[item[2]] += 1
    Accuracy = {key: value / key_counts[key] for key, value in Accuracy.items()}
    return Accuracy


def get_topK_prompt(results, k):
    accuracy_dict = evaluate_test(results)
    sorted_keys = sorted(accuracy_dict, key=lambda x: accuracy_dict[x][2], reverse=True)[:k]
    topK_accuracy_dict = {key: accuracy_dict[key] for key in sorted_keys}
    return topK_accuracy_dict


def evaluate_test(results):
    template_dict = {}
    for result in results:
        template_dict[result[2]] = [[], []]
    for result in results:
        template_dict[result[2]][0].append(result[1])
        template_dict[result[2]][1].append(result[3])
    accuracy_dict = {}
    for key in template_dict.keys():
        ga, fga = calculate_ga_fga(covertListToDataFrame(template_dict[key][0], 'EventTemplate'),
                                   covertListToDataFrame(template_dict[key][1], 'EventTemplate'))
        pa = calculate_pa(covertListToDataFrame(template_dict[key][0], 'EventTemplate'),
                          covertListToDataFrame(template_dict[key][1], 'EventTemplate'))
        accuracy_dict[key] = [ga, fga, pa]
    return accuracy_dict


# 获取测试集合或者训练集合的准确率，pa,ga,fga
def calculate_accuracy_test(test_contents, test_templates, selected_k_prompt):
    results = extract_log_template(test_contents, test_templates, selected_k_prompt)
    accuracy_dict = evaluate_test(results)
    return accuracy_dict


if __name__ == '__main__':
    # print(evaluate_test(get_test_results()))
    # for i in evaluate_test(get_test_results()).items():
    #     print(i)
    origin = "Address change detected. Old: msra-sa-41/10.190.173.170:9000 New: msra-sa-41:9000"
    a = "Address change detected. Old: <*>/<*>:<*> New: <*>:<*>"
    b = "Address change detected. Old: <*> New: <*>"
    print(correct_lstm(a, b))
