import concurrent.futures

from benchmark.IPRE.AutoPrompt.selectLog import get_train_dataSet
from src.LogModule.AutoPrompt.promptApi import infer_llm
from src.config.configLoad import load_config


def generation_prompt(gpt_prompts):
    # 这里是依据示例，来生成初始提示词

    prompt = (f"you would summarize the process of identify relation between entities based on given "
              f" context to help other language model "
              f"assistants improve the accuracy of relation identification"
              f"Do not be overprecise to the example below. ") + get_random_log(2)
    response = infer_llm(prompt, None, None, temperature=1.0)
    if response != "404ERROR":
        gpt_prompts.append(response)


def get_random_log(num: int):  # Input, Output = get_random_log(2, load_config("BaseFile"))
    pd = get_train_dataSet()
    new_pd = pd.sample(n=num)
    text = "This is example:\n"
    for _,row in new_pd.iterrows():
        text += "<Example>"+(f"EntityA: <START>{row[0]}<END>\n"
                 f"EntityB: <START>{row[1]}<END>\n"
                 f"Context: <START>{row[2].replace(' ','')}<END>\n"
                 f"Relation: <START>{row[3]}<END>\n") +"</Example>"
    return text


def taskMakePrompt(gpt_prompts):
    generation_prompt(gpt_prompts)


def init_prompt(promptsNum: int):
    gpt_prompts = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=load_config("ThreadNum")) as executor:
        futures = []
        for i in range(promptsNum):
            future = executor.submit(taskMakePrompt,gpt_prompts)
            futures.append(future)
        concurrent.futures.wait(futures)
    print("gpt生成的提示词:", gpt_prompts)
    return gpt_prompts


if __name__ == '__main__':
    print(init_prompt(2))
