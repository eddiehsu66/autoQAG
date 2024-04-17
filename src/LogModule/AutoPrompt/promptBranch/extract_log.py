import re

from src.LogModule.CasePrompt.promptSelect import prompt_select
from src.LogModule.AutoPrompt.promptApi import infer_llm
from src.config.redisKit import redisInit
from src.evaluation.accuracy import correct_lstm
import concurrent.futures
from src.config.configLoad import load_config

BaseFile = load_config("BaseFile")


def TaskExtractLog(log_content, prompt, log_template):
    result_item = []
    prompt_temp = "You will be provided with a log message." \
                  f"log message:{log_content}," \
                  f"{prompt}" \
                  f"Output according to the above requirement, without any superfluous output" \
                  f"Please follow the example below to extract the log template: \n"
    similiar_log = prompt_select(log_content, 5, BaseFile)
    for item in similiar_log:
        prompt_temp += f"Log message: <START>{item['Content']}<END>" \
                       f"Log template: <START>{item['answer']}<END> \n"
    client = redisInit()
    response = client.get(prompt_temp)
    if response is None:
        response = infer_llm(prompt_temp, None, None, cached=False)
    parsedLog = parse_log(response)
    if correct_lstm(parsedLog,log_template):
        client.set(prompt_temp,response)
    if response != "404ERROR":
        result_item.append(log_content)
        result_item.append(log_template)
        result_item.append(prompt)
        result_item.append(parsedLog)
    return result_item


def extract_log_template(log_contents, log_templates, prompts):
    result = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=load_config("ThreadNum")) as executor:
        futures = []
        for index, log_content in enumerate(log_contents):
            for prompt in prompts:
                future = executor.submit(TaskExtractLog, log_content, prompt, log_templates[index])
                futures.append(future)
        for future in concurrent.futures.as_completed(futures):
            if len(future.result()) != 0:
                # print(future.result())
                result.append(future.result())
    return result


def parse_log(log):
    match = re.search(r'(?<=Log template: ).*', log)
    if match:
        content = match.group(0)
        return content.replace("\n", "").replace("<END>", "").replace("<START>", "")
    return log.replace("\n", "").replace("<END>", "").replace("<START>", "")


if __name__ == '__main__':
    print(parse_log("这是一段文本，其中包含Log template: 需要提取的日志模板内容"))
