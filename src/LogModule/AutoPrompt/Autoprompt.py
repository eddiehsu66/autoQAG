import time
from src.LogModule.AutoPrompt.promptBranch.SamanticPrompts import generate_samantic_prompts
from src.LogModule.AutoPrompt.selectLog import get_train_log, get_test_log
from src.LogModule.AutoPrompt.draw import draw_plot_with_keys
from src.LogModule.AutoPrompt.promptBranch.extract_log import extract_log_template
from src.LogModule.AutoPrompt.promptBranch.init_prompt import init_prompt
from src.evaluation.accuracy import get_topK_prompt, calculate_accuracy_test


# 从gpt生成的提示词中挑选前k个提示词


if __name__ == '__main__':
    train_accuracy_asset = []
    test_accuracy_asset = []

    start_time = time.time()
    k = 5  # 从gpt生成的提示词中挑选前k个提示词
    m = 2  # 挑选出来的前K个提示词坐同语义处理，每个提示词生成m个同语义的提示词
    overall_number_of_cycles = 3  # 整体循环次数

    train_contents, train_templates = get_train_log()
    test_contents, test_templates = get_test_log()
    cur_prompts = init_prompt(10)
    # 第一轮次
    # 由gpt生成的提示词来抽取模版
    results = extract_log_template(train_contents, train_templates, cur_prompts)

    topK_prompt = get_topK_prompt(results,5)
    topK_prompt_list = list(topK_prompt.keys())
    train_accuracy_asset.append(topK_prompt)
    test_accuracy_asset.append(calculate_accuracy_test(test_contents, test_templates,topK_prompt_list))
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
        print(f"第{i+2}轮挑选的提示词以及其精度:", topK_prompt)
        samantic_prompts = generate_samantic_prompts(topK_prompt_list, results)
        print(f"第{i+2}轮生成的同语义的提示词:", samantic_prompts)

    end_time = time.time()
    elapsed_time = end_time - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    print(f"程序运行时间为: {minutes} 分钟 {seconds} 秒")
    draw_plot_with_keys(test_accuracy_asset)
    print("train_accuracy_asset:")
    print(train_accuracy_asset)
