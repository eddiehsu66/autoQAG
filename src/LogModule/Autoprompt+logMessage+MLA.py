import concurrent.futures
import csv
import random
import time
from src.LogModule.promptApi import infer_llm
from src.LogModule.selectLog import selectLog

androidPath = r'C:\code\src\python\autoQAG\data\loghub-master\Android'

ThreadNum = 6


# 输入两个列表，第一个是原始log，第二个是标准模版，第三个是循环次数
def gerneration_prompt(input, output, number):
    text = ""
    for i in range(len(input)):
        text += "Input:" + input[i] + ", " + "Output:" + output[i] + '\n'

    # 由gpt生成日志解析模版，输出模版放在提示词的最后面
    prompt1 = "I gave a friend an instruction and five inputs. " \
              "The friend read the instruction and wrote an output for every one of the inputs. " \
              f"Here are the input-outputpairs: \n{text}" \
              f"Please output my instruction to the friend, only instruction, without any superfluous output"

    # 由gpt生成日志解析模版，输出模版放在提示词的中间
    prompt2 = "I instructed my friend to <>. " \
              "The friend read the instruction and wrote an output for every one of the inputs. " \
              f"Here are the input-outputpairs: \n{text}" \
              f"Please output my instruction to the friend, only instruction, without any superfluous output" \
 \
        # 由gpt生成日志解析模版，输出模版放在提示词的中间
    prompt3 = "Professor Smith was given the following instruction:<>" \
              f"Here are the Professor's responses: \n{text} " \
              f"Please output the instruction, only instruction, without any superfluous output"

    prompts = [prompt1, prompt2, prompt3]

    response = infer_llm(prompts[0], None, None)
    gpt_prompts.append(response)
    print("gpt生成的提示词:", response)


# 随机抽取原始日志，创建input和output
# number：随机抽取的数据条数

# 验证集方式优化，n论m个提示词，取出前k个最好的，然后对这k个提示词做同义处理，每个提示词生成m个同义的提示词，B+1个提示词
def random_select_log(number):
    input = []
    output = []
    with open(androidPath + r'\Android_2k.log', 'r') as file:
        lines = file.readlines()
        line_count = len(lines)
        # 随机抽取number个数据
        random_index = random.sample(range(line_count), number)
        for index in random_index:
            # input.append(lines[index])
            with open(androidPath + r'\Android_2k.log_structured.csv', 'r') as csvfile:
                # 创建 CSV 文件读取器
                reader = csv.reader(csvfile)
                template_list = list(reader)
                for index1, element in enumerate(template_list[index + 1]):
                    if element.startswith('E') and element[1:].isdigit():
                        output.append(template_list[index + 1][index1 + 1])
                        input.append(template_list[index + 1][index1 - 1])
    return input, output


# 由gpt生成的提示词去抽取日志模版
# 输入初始log内容，标准模版以及gpt生成的提示词
def TaskExtractLog(log_content, prompt, log_template):
    result_item = []
    prompt_temp = "You will be provided with a log message." \
                  f"{log_content}" \
                  f"{prompt}" \
                  f"Output according to the above requirement, without any superfluous output"
    response = infer_llm(prompt_temp, None, None)
    result_item.append(log_content)
    result_item.append(log_template)
    result_item.append(prompt)
    result_item.append(response)
    return result_item


def extract_log_template(log_contents, log_templates, prompts):
    # 存储结果 初始log内容，该log的标准模版，gpt生成的提示词，gpt抽取的日志模版
    # result = []
    # for index, log_content in enumerate(log_contents):
    #     for prompt in prompts:
    #         result_item = []
    #         # 让gpt去抽取日志模版的提示词
    #         prompt_temp = "You will be provided with a log message." \
    #                       f"{log_content}" \
    #                       f"{prompt}" \
    #                       f"Output according to the above requirement, without any superfluous output"
    #         response = infer_llm("", prompt_temp, "", None, "")
    #         result_item.append(log_content)
    #         result_item.append(log_templates[index])
    #         result_item.append(prompt)
    #         result_item.append(response)
    #         result.append(result_item)
    #         print(result_item)
    result = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=ThreadNum) as executor:
        futures = []
        for index, log_content in enumerate(log_contents):
            for prompt in prompts:
                future = executor.submit(TaskExtractLog, log_content, prompt, log_templates[index])
                futures.append(future)
        for future in concurrent.futures.as_completed(futures):
            try:
                # 添加异常处理
                print(future.result())
                result.append(future.result())
            except Exception as e:
                print(f"TaskExtractLog任务执行失败: {e}")
    return result


# 统计gpt生成的提示词的效果，由一个字典存储，{prompt: accuracy}
# 输入：gpt生成的提示词, 由gpt生成的提示词生成的结果，一个gpt生成的提示词用log_number个log来检验效果
def prompt_accuracy_count(gpt_prompts, results, log_number):
    Accuracy = {gpt_prompt: 0 for gpt_prompt in gpt_prompts}
    print("初始精度：", Accuracy)
    for index, item in enumerate(results):
        if item[1] == item[3]:
            Accuracy[item[2]] += 1
            # print(index)
    Accuracy = {key: value / log_number for key, value in Accuracy.items()}
    return Accuracy


# 从gpt生成的提示词中挑选前k个提示词
def select_prompt(accuracy_dict, k):
    sorted_keys = sorted(accuracy_dict, key=lambda x: accuracy_dict[x], reverse=True)[:k]
    return sorted_keys


def TaskSamanticPrompts(prompt, m):
    prompt_temp = f"According to the following prompt, {m} prompts are generated while maintaining the same semantics" \
                  f"The prompt is {prompt}" \
                  f"The generated prompts without any superfluous output" \
                  f"For example:1.Prompt1\n2.Prompt2"
    response = infer_llm(prompt_temp, None, None)
    print(prompt + ":", response + '\n')
    list_temp = []
    for item in response.split('\n'):
        list_temp.append(item[2:])
    return list_temp


def generate_samantic_prompts(prompts, m):
    semantic_prompts = prompts[:]

    # for prompt in prompts:
    #     prompt_temp = f"According to the following prompt, {m} prompts are generated while maintaining the same semantics" \
    #                   f"The prompt is {prompt}" \
    #                   f"The generated prompts without any superfluous output" \
    #                   f"For example:1.Prompt1\n2.Prompt2"
    #     # pattern = r'^[0-9.]*([\w\s]+)*$'
    #
    #     response = infer_llm("", prompt_temp, "", None, "")
    #     print(prompt, ":", response + '\n')
    #     list_temp = []
    #     for item in response.split('\n'):
    #         # match = re.match(pattern, item)
    #         # if match:
    #         list_temp.append(item[2:])
    #     semantic_prompts += list_temp
    futures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=ThreadNum) as executor:
        # 对于每个提示，使用submit方法提交处理任务
        for prompt in prompts:
            future = executor.submit(TaskSamanticPrompts, prompt, m)
            futures.append(future)
        concurrent.futures.wait(futures)
        # 等待所有Future对象完成，并收集结果
        for future in concurrent.futures.as_completed(futures):
            semantic_prompts += future.result()
    return semantic_prompts


def taskMakePrompt():
    Input, Output = random_select_log(log_prompt_number)
    gerneration_prompt(Input, Output, i)


if __name__ == '__main__':

    start_time = time.time()
    gpt_prompts = []  # 装gpt生成的模版
    gpt_prompts_number = 20  # gpt生成的初始模版条数
    log_number = 50  # 一个gpt生成的提示词用log_number个log来检验效果
    log_prompt_number = 5  # 喂给gpt产生提示词的log数量
    k = 5  # 从gpt生成的提示词中挑选前k个提示词
    m = 2  # 挑选出来的前K个提示词坐同语义处理，每个提示词生成m个同语义的提示词
    overall_number_of_cycles = 20  # 整体循环次数

    # for i in range(gpt_prompts_number):
    #     Input, Output = random_select_log(log_prompt_number)
    #     # 产生gpt提示词
    #     gerneration_prompt(Input, Output, i)

    # 多线程生成gpt提示词
    with concurrent.futures.ThreadPoolExecutor(max_workers=ThreadNum) as executor:
        futures = []
        for i in range(gpt_prompts_number):
            future = executor.submit(taskMakePrompt)
        concurrent.futures.wait(futures)

    # log_contents, log_templates = random_select_log(log_number)
    log_contents, log_templates = selectLog(0, 32)
    # 由gpt生成的提示词来抽取模版
    results = extract_log_template(log_contents, log_templates, gpt_prompts)

    # 统计gpt生成的提示词的效果，由一个字典存储，{prompt: accuracy}
    accuracy_dict = prompt_accuracy_count(gpt_prompts, results, log_number)
    print("第1轮的精度：", accuracy_dict)
    # 从gpt生成的提示词中挑选前k个提示词
    selected_k_prompt = select_prompt(accuracy_dict, k)
    print("第1轮挑选的提示词:", selected_k_prompt)

    # selected_k_prompt_temp = ['Remove sensitive information from the inputs.', 'Remove sensitive information and limit output.']

    # 挑选出来的前K个提示词做同语义处理，每个提示词生成m个同语义的提示词
    samantic_prompts = generate_samantic_prompts(selected_k_prompt, m)
    print("第1轮保留的同语义的提示词:", samantic_prompts)
    print("第1轮保留的同语义的提示词长度:", len(samantic_prompts))

    # 在n-1论测试集合
    for i in range(overall_number_of_cycles):
        # 随机抽取原始日志 用于测试-》验证集合
        log_contents, log_templates = selectLog(i + 1, 32)
        # 由gpt生成的提示词去抽取日志模版
        results = extract_log_template(log_contents, log_templates, samantic_prompts)
        # 统计gpt生成的提示词的效果，由一个字典存储，{prompt: accuracy}
        accuracy_dict = prompt_accuracy_count(samantic_prompts, results, log_number)
        print(f"第{i + 2}轮的精度：{accuracy_dict}")
        selected_k_prompt = select_prompt(accuracy_dict, k)
        print(f"第{i + 2}轮挑选的提示词：", selected_k_prompt)
        samantic_prompts = generate_samantic_prompts(selected_k_prompt, m)
        print(f"第{i + 2}轮保留的同语义的提示词：", samantic_prompts)
        print(f"第{i + 2}轮保留的同语义的提示词长度：", len(samantic_prompts))

    end_time = time.time()
    elapsed_time = end_time - start_time

    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)

    print(f"程序运行时间为: {minutes} 分钟 {seconds} 秒")