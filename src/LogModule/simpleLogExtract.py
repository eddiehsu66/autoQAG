import os
import re
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd

from src.LogModule.logSelector import select_candidateSampleLog
from src.config.openaiKit import infer_llm
import concurrent.futures
from src.config.configLoad import load_config
from src.config.redisKit import redisInit


def TaskExtractLog(category, uuid, row, prompt):
    log_content = row['Content']
    prompt_temp = "You will be provided with a log message." \
                  f"log message:{log_content}," \
                  f"{prompt}" \
                  f"Output according to the above requirement, without any superfluous output" \
                  f"Please follow the example below to extract the log template: \n"
    similiar_log = select_candidateSampleLog(category, uuid, log_content, 3)
    for item in similiar_log:
        prompt_temp += f"Log message: <START>{item['Content']}<END>" \
                       f"Log template: <START>{item['answer']}<END> \n"
    # client = redisInit()
    # response = client.get("llmPrompt:" + prompt_temp)
    # if response is None:
    #     response = infer_llm(prompt_temp, None, None)
    #     if response == "404ERROR":
    #         exit()
    #     client.set("llmPrompt:" + prompt_temp, response)
    response = infer_llm(prompt_temp, None, None)
    parsedLog = parse_log(response)
    df = pd.DataFrame(columns=row.index)
    df.loc[row.name] = row
    df.loc[row.name, 'EventTemplate'] = parsedLog
    content = row['Content']
    client = redisInit()
    client.sadd('LogTemplate:' + uuid + ':' + str(parsedLog), content)
    return df.loc[row.name]


def extract_log_template(category, uuid, subset, prompt):
    subset = subset.apply(lambda row: TaskExtractLog(category, uuid, row, prompt), axis=1)
    return subset


def parse_log(log):
    match = re.search(r'(?<=Log template: ).*', log)
    if match:
        content = match.group(0)
        return content.replace("\n", "").replace("<END>", "").replace("<START>", "").replace("`", "").replace("\"", "")
    return log.replace("\n", "").replace("<END>", "").replace("<START>", "").replace("`", "").replace("\"", "")


def simple_log_extract(category, uuid):
    aim_log = pd.read_csv(f"../../cache/logs/{uuid}/Test_parsed.csv")
    prompt = ("I want you to act like an expert of log parsing. "
              "I will give you a log message. "
              "You must identify and abstract all the dynamic variables in logs <*>"
              "and output a log template")
    num_works = load_config("ThreadNum")
    template_path = f"../../cache/logs/{uuid}/Test_template.csv"
    if not os.path.exists(template_path):
        aim_log['EventTemplate'] = None

        aim_log_subsets = [aim_log.iloc[i::num_works] for i in range(num_works)]

        with ThreadPoolExecutor(max_workers=num_works) as executor:
            results = executor.map(lambda subset: extract_log_template(category, uuid, subset, prompt), aim_log_subsets)

        pd.concat(results).to_csv(template_path, index=False)


if __name__ == '__main__':
    simple_log_extract("Test",
                       'fb5c5335-566b-49cc-88a1-d563d1bc68fa')
