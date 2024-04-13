import random

from src.LogModule.AutoPrompt.promptApi import infer_llm
import concurrent.futures
from src.config.configLoad import load_config
from src.LogModule.AutoPrompt.promptBranch.wrongReason import batchProcess
from src.evaluation.accuracy import correct_lstm


def TaskSamanticPrompts(prompt, wrong_reason):
    prompt1 = f"According to the following prompt, prompts are generated while maintaining the same semantics" \
              f"The prompt is {prompt}" \
              f"This is the reason for the error that occurred during the previous parsing of the log :{wrong_reason}" \
              f"The generated prompts without any superfluous output"

    prompt2 = (f"There is currently a prompt word for log parsing, "
               f"The prompt word is <START>{prompt}<END>,"
               f"but the prompt word is currently not effective enough. "
               f"It may be due to the following reasons: <START>{wrong_reason}<END>"
               f"Please update the prompts and modify with out any superfluous output")

    prompt3 = (f"This is a log parse Task, and our task is Ineffective"
               f"These are some possible reasons for poor performance: <START>{wrong_reason}<END>"
               f"Based on the prompt word <START>{prompt}<END>, generate a new prompt word with the same semantics")
    prompts = [prompt1, prompt2, prompt3]
    list_temp = []
    response = infer_llm(prompt[0], None, None)
    if response != "404ERROR":
        list_temp.append(response)
    return list_temp


def generate_samantic_prompts(prompts, result):
    semantic_prompts = prompts[:]
    futures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=load_config("ThreadNum")) as executor:
        # 对于每个提示，使用submit方法提交处理任务
        for prompt in prompts:
            wrongReason = warp_wrongReason(result, prompt)
            future = executor.submit(TaskSamanticPrompts, prompt, wrongReason)
            futures.append(future)
        concurrent.futures.wait(futures)
        # 等待所有Future对象完成，并收集结果
        for future in concurrent.futures.as_completed(futures):
            semantic_prompts += future.result()
    return semantic_prompts


def warp_wrongReason(results: list, prompt: str):
    wrong_data = []
    for item in results:
        if item[2] == prompt and not correct_lstm(item[1], item[3]):
            wrong_data.append(item)
    return batchProcess(wrong_data)
