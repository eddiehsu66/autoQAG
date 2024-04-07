from src.LogModule.CasePrompt.promptSelect import prompt_select
from src.LogModule.AutoPrompt.promptApi import infer_llm
import concurrent.futures
from src.config.configLoad import load_config


def TaskExtractLog(log_content, prompt, log_template):
    result_item = []
    prompt_temp = "You will be provided with a log message." \
                  f"log message:{log_content}," \
                  f"{prompt}" \
                  f"Output according to the above requirement, without any superfluous output" \
                  f"Please follow the example below to extract the log template: \n"
    similiar_log = prompt_select(log_content, 5)
    for item in similiar_log:
        prompt_temp += f"Log message: <START>{item['Content']}<END>" \
                       f"Log template: <START>{item['answer']}<END> \n"
    response = infer_llm(prompt_temp, None, None, cached=True)
    result_item.append(log_content)
    result_item.append(log_template)
    result_item.append(prompt)
    result_item.append(parse_log(response))
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
            print(future.result())
            result.append(future.result())
    return result


def parse_log(log):
    try:
        return log.split("Log template: ")[1].replace("\n", "").replace("<END>", "").replace("<START>", "")
    except Exception as e:
        return log