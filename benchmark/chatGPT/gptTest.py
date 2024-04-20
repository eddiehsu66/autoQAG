import csv
import openai
import os
import json
from src.LogModule.AutoPrompt.promptApi import infer_llm
from src.evaluation.accuracy import evaluate_test
from src.LogModule.AutoPrompt.promptBranch.init_prompt import generation_prompt
prompt1 = "Replace all specific values with <*> in the given input:"
prompt2 = "Anonymize the following input:"
prompt3 = ("I want you to act like an expert of log parsing. "
                    "I will give you a log message delimited by backticks. "
                    "You must identify and abstract all the dynamic variables in logs with {*} "
                    "and output a static log template. Print the input log's template delimited by backticks.")
prompt4 = "Extract one log template, substitute variable tokens in the log as <*> tags,output the log template."


# openai.api_base = os.getenv("OPENAI_API_BASE", OPENAI_API_BASE)


def makeExample(input, output):
    text = "This is example:\n"
    for i in range(len(input)):
        text += (f"LogMessage: <START>{input[i]}<START>\n"
                 f"LogTemplate: <START>{output[i]}<START>\n")
    return text


def get_test_results(fileName:str):
    input = ['Created MRAppMaster for application appattempt_1445144423722_0020_000001',
             'Default file system [hdfs://msra-sa-41:9000]']
    output = ['Created MRAppMaster for application appattempt_<*>', 'Default file system [hdfs://<*>:<*>']
    gpt_prompts = []
    prompts = generation_prompt(input,output,1,gpt_prompts)

    path = rf"C:\code\src\python\autoQAG\data\loghub-master\{fileName}\{fileName}_2k.log_testData.csv"
    with open(path, 'r') as file:
        # 创建CSV阅读器对象
        csv_reader = csv.reader(file)
        data_list = list(csv_reader)
        # 遍历每一行，并将第7列数据存储在一个列表中
        column_7_data = [row[11] for row in data_list]
        column_9_data = [row[13] for row in data_list]
        dict_output = {}
        for prompt in gpt_prompts:
            list_output = []
            for index, content in enumerate(column_7_data):
                data = [content, column_9_data[index], prompt]
                prompt_temp = prompt + content
                response = infer_llm(prompt_temp, None, None)
                data.append(response)
                list_output.append(data)
            dict_output[prompt] = evaluate_test(list_output)
    return dict_output


if __name__ == '__main__':
    print(get_test_results("Thunderbird"))
