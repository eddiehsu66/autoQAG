import concurrent.futures

from src.LogModule.AutoPrompt.promptApi import infer_llm
from src.LogModule.AutoPrompt.selectLog import get_random_log
from src.config.configLoad import load_config


def generation_prompt(input, output, order, gpt_prompts):
    # 这里是依据示例，来生成初始提示词

    prompt1 = (f"The assistant can summarize this process based on given "
               f"examples from logs to templates to help other language model"
               f"assistants improve the accuracy of log template parsing base your given prompt."
               f"Do not be overprecise to the example. \n") + makeExample(input, output)

    prompt2 = (f"Based on the given examples, the assistant can summarize the"
               f" process from logs to templates to help other language model "
               f"assistants improve the accuracy of log template parsing."
               f"Do not be overprecise to the example. \n") + makeExample(input, output)

    prompts = [prompt1, prompt2]
    response = infer_llm(prompts[order % len(prompts)], None, None, temperature=1.0)
    gpt_prompts.append(response)
    # print("gpt生成的提示词:", response)
    return gpt_prompts


def makeExample(input, output):
    text = "This is example:\n"
    for i in range(len(input)):
        text += (f"LogMessage: <START>{input[i]}<START>\n"
                 f"LogTemplate: <START>{output[i]}<START>\n")
    return text


def taskMakePrompt(order, gpt_prompts):
    Input, Output = get_random_log(2)
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
