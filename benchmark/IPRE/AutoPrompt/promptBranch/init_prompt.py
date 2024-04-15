import concurrent.futures

from src.LogModule.AutoPrompt.promptApi import infer_llm


def generation_prompt(input, output, order, gpt_prompts):
    # 这里是依据示例，来生成初始提示词

    prompt = (f"The assistant can summarize this process based on given "
               f"examples from logs to templates to help other language model"
               f"assistants improve the accuracy of log template parsing base your given prompt."
               f"Do not be overprecise to the example. \n") + makeExample(input, output)

    response = infer_llm(prompt, None, None, temperature=1.0)
    if response != "404ERROR":
        gpt_prompts.append(response)


def makeExample(input, output):
    text = "This is example:\n"
    for i in range(len(input)):
        text += (f"LogMessage: <START>{input[i]}<START>\n"
                 f"LogTemplate: <START>{output[i]}<START>\n")
    return text


def taskMakePrompt(order, gpt_prompts):
    Input, Output = get_random_log(2, load_config("BaseFile"))
    generation_prompt(Input, Output, order, gpt_prompts)


def init_prompt(promptsNum: int):
    gpt_prompts = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=load_config("ThreadNum")) as executor:
        futures = []
        for i in range(promptsNum):
            future = executor.submit(taskMakePrompt, i, gpt_prompts)
            futures.append(future)
        concurrent.futures.wait(futures)
    print("gpt生成的提示词:", gpt_prompts)
    return gpt_prompts


if __name__ == '__main__':
    print(len(init_prompt(10)))
