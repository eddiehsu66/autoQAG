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
    overall_number_of_cycles = 10  # 整体循环次数

    train_contents, train_templates = get_train_log(BaseFile)
    test_contents, test_templates = get_test_log(BaseFile)
    cur_prompts = init_prompt(10)
    # 第一轮次
    # 由gpt生成的提示词来抽取模版
    results = extract_log_template(train_contents, train_templates, cur_prompts)

    topK_prompt = get_topK_prompt(results, 5)
    topK_prompt_list = list(topK_prompt.keys())
    train_accuracy_asset.append(topK_prompt)
    test_accuracy_asset.append(calculate_accuracy_test(test_contents, test_templates, topK_prompt_list))
    print("第1轮挑选的提示词以及其精度:", topK_prompt)
    samantic_prompts = generate_samantic_prompts(topK_prompt_list, results)
    print("第1轮生成的同语义的提示词:", samantic_prompts)

    # 在n-1论测试集合
    for i in range(overall_number_of_cycles):
        # 由gpt生成的提示词去抽取日志模版
        results = extract_log_template(train_contents, train_templates, samantic_prompts)

        topK_prompt = get_topK_prompt(results, 5)
        topK_prompt_list = list(topK_prompt.keys())
        train_accuracy_asset.append(topK_prompt)
        test_accuracy_asset.append(calculate_accuracy_test(test_contents, test_templates, topK_prompt_list))
        print(f"第{i + 2}轮挑选的提示词以及其精度:", topK_prompt)
        samantic_prompts = generate_samantic_prompts(topK_prompt_list, results)
        print(f"第{i + 2}轮生成的同语义的提示词:", samantic_prompts)

    end_time = time.time()
    elapsed_time = end_time - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    print(f"程序运行时间为: {minutes} 分钟 {seconds} 秒")
    print("train_accuracy_asset:")
    print(test_accuracy_asset)

    draw_plot_with_keys(test_accuracy_asset)
    draw_plotBox(test_accuracy_asset)
    save_csv(test_accuracy_asset)


if __name__ == '__main__':
    candidateSample(1024, 'others')
    random_select_log(300)
    candidateSample(32, 'sampled')
    auto_prompt()
