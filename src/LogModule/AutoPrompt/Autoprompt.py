import time

import pandas as pd

from src.LogModule.AutoPrompt.promptBranch.SamanticPrompts import generate_samantic_prompts
from src.LogModule.AutoPrompt.selectLog import get_train_log, get_test_log, candidateSample, random_select_log
from src.LogModule.AutoPrompt.draw import draw_plot_with_keys, draw_plotBox
from src.LogModule.AutoPrompt.promptBranch.extract_log import extract_log_template
from src.LogModule.AutoPrompt.promptBranch.init_prompt import init_prompt
from src.config.configLoad import load_config
from src.evaluation.accuracy import get_topK_prompt, calculate_accuracy_test

BaseFile = load_config("BaseFile")


def save_csv(data):
    path = "C:/code/src/python/autoQAG/result/accuracy.csv"
    rows = []
    # 遍历data中的每个元素（假设每个元素是一个字典）
    for i, item in enumerate(data):
        for key, values in item.items():
            row = {'order': i, 'prompt': key, 'ga': values[0], 'fga': values[1], 'pa': values[2]}
            rows.append(row)
    df = pd.DataFrame(rows)
    df.to_csv(path, index=False, encoding='utf-8')


def auto_prompt():
    train_accuracy_asset = []
    test_accuracy_asset = []

    start_time = time.time()
    overall_number_of_cycles = 2  # 整体循环次数

    train_contents, train_templates = get_train_log(BaseFile)
    test_contents, test_templates = get_test_log(BaseFile)
    cur_prompts = init_prompt(10)
    # 第一轮次
    # 由gpt生成的提示词来抽取模版
    results = extract_log_template(train_contents, train_templates, cur_prompts)

    topK_prompt = get_topK_prompt(results, 5)
    topK_prompt_list = list(topK_prompt.keys())
    train_accuracy_asset.append(topK_prompt)
    # test_accuracy_asset.append(calculate_accuracy_test(test_contents, test_templates, topK_prompt_list))
    print("第1轮挑选的提示词以及其精度:", topK_prompt)
    samantic_prompts = generate_samantic_prompts(topK_prompt_list, results)
    print("第1轮生成的同语义的提示词:", samantic_prompts)
    print("z第一轮结束zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz")
    # 在n-1论测试集合
    for i in range(overall_number_of_cycles):
        # 由gpt生成的提示词去抽取日志模版
        results = extract_log_template(train_contents, train_templates, samantic_prompts)

        topK_prompt = get_topK_prompt(results, 5)
        topK_prompt_list = list(topK_prompt.keys())
        train_accuracy_asset.append(topK_prompt)
        # test_accuracy_asset.append(calculate_accuracy_test(test_contents, test_templates, topK_prompt_list))
        print(f"第{i + 2}轮挑选的提示词以及其精度:", topK_prompt)
        samantic_prompts = generate_samantic_prompts(topK_prompt_list, results)
        print(f"第{i + 2}轮生成的同语义的提示词:", samantic_prompts)

        draw_plot_with_keys(train_accuracy_asset)
        draw_plotBox(train_accuracy_asset)
        save_csv(train_accuracy_asset)
        print(f"zz第{i+2}轮结束zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz")

    test_accuracy = calculate_accuracy_test(test_contents, test_templates, topK_prompt_list)
    print("最后的结果所测试精度:", test_accuracy)
    print("zz")
    print("总的训练集合精度:", train_accuracy_asset)
    end_time = time.time()
    elapsed_time = end_time - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    print(f"程序运行时间为: {minutes} 分钟 {seconds} 秒")


if __name__ == '__main__':
    # candidateSample(1024, 'others')
    # random_select_log(300)
    # candidateSample(32, 'sampled')
    auto_prompt()
    # topK_dict = {'The process of parsing log messages into log templates involves identifying key patterns and placeholders within the log messages. This can include marking specific keywords or phrases that are consistently present in the log messages and replacing dynamic values with placeholders. By creating a standardized log template format, language model assistants can improve accuracy and efficiency in parsing log messages for various applications.': [0.8037037037037037, 0.7719298245614036, 0.9], 'The process of converting log messages to log templates involves identifying recurring patterns in the log messages and replacing specific values with placeholders. This allows language model assistants to better understand and parse log data for improved accuracy and efficiency.': [0.9, 0.8214285714285714, 0.9], 'The process involves analyzing log messages to identify patterns and create log templates. The templates are used to extract structured information from future log messages with similar patterns, improving accuracy and efficiency in parsing log data for language model assistants.': [0.8037037037037037, 0.8, 0.9], 'The process of log template parsing involves identifying key patterns and placeholders in log messages and creating a generalized template that can be used to match similar log messages. By analyzing multiple examples of log messages, such as the ones provided, language model assistants can identify common patterns, such as specific keywords and variable placeholders, and create templates that capture these patterns. These templates can then be used to parse and extract relevant information from new log messages with similar structures, improving the accuracy of log analysis and information retrieval.': [0.8037037037037037, 0.8148148148148148, 0.9], '1. The error during the previous log parsing occurred because the model incorrectly identified specific user information and additional authentication failure details instead of simply identifying the repeated log message.\n2. The error during the previous log parsing occurred because the model mistakenly focused on extracting specific variable values instead of understanding the overall context of the log message.\n3. The error during the previous log parsing occurred because the model is incorrectly filling in placeholders "<*>" with redundant and repetitive information from the logContent.': [0.8037037037037037, 0.8148148148148148, 0.8962962962962963]}
    # topK_prompt_list = list(topK_dict.keys())
    # test_contents, test_templates = get_test_log(BaseFile)
    # test_accuracy = calculate_accuracy_test(test_contents, test_templates, topK_prompt_list)
    # print("最后的结果所测试精度:", test_accuracy)
