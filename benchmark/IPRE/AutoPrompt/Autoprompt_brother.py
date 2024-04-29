import time

import pandas as pd

from benchmark.IPRE.AutoPrompt.promptBranch.SamanticPrompts import generate_samantic_prompts
from benchmark.IPRE.AutoPrompt.draw import draw_plot_with_keys, draw_plotBox
from benchmark.IPRE.AutoPrompt.promptBranch.extract_log import extract_log_template
from benchmark.IPRE.AutoPrompt.promptBranch.init_prompt import init_prompt
from benchmark.IPRE.evaluation.accuracy import calculate_multiclass_metrics_sklearn, get_topK_prompt_accuracy
from src.config.configLoad import load_config



def auto_prompt():
    train_accuracy_asset = []
    test_accuracy_asset = []

    start_time = time.time()
    overall_number_of_cycles = 1  # 整体循环次数

    cur_prompts = init_prompt(10)
    # 第一轮次
    # 由gpt生成的提示词来抽取模版
    results = extract_log_template(cur_prompts)

    topK_prompt = get_topK_prompt_accuracy(results, 5)
    topK_prompt_list = list(topK_prompt.keys())
    train_accuracy_asset.append(topK_prompt)
    print("第1轮挑选的提示词以及其精度:", topK_prompt)
    samantic_prompts = generate_samantic_prompts(topK_prompt_list, results)
    print("第1轮生成的同语义的提示词:", samantic_prompts)

    # 在n-1论测试集合
    for i in range(overall_number_of_cycles):
        results = extract_log_template(samantic_prompts)
        topK_prompt = get_topK_prompt_accuracy(results, 5)
        topK_prompt_list = list(topK_prompt.keys())
        train_accuracy_asset.append(topK_prompt)
        print(f"第{i + 2}轮挑选的提示词以及其精度:", topK_prompt)
        samantic_prompts = generate_samantic_prompts(topK_prompt_list, results)
        print(f"第{i + 2}轮生成的同语义的提示词:", samantic_prompts)

        # draw_plot_with_keys(test_accuracy_asset)
        # draw_plotBox(test_accuracy_asset)
        # save_csv(test_accuracy_asset)

    testResults = extract_log_template(topK_prompt_list,'test')
    with open(rf"C:\code\src\python\autoQAG\result\ipre_testResult_{load_config('BaseObject')}.txt", "w", encoding='utf-8') as file:
        file.write(str(testResults))
    print("内容已写入到 output.txt 文件中。")
    print(calculate_multiclass_metrics_sklearn(testResults))
    end_time = time.time()
    elapsed_time = end_time - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    print(f"程序运行时间为: {minutes} 分钟 {seconds} 秒")
    print("train_accuracy_asset:")


if __name__ == '__main__':
    # candidateSample(1024, 'others')
    # random_select_log(300)
    # candidateSample(32, 'sampled')
    auto_prompt()
