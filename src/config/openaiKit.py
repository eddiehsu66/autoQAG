from openai import OpenAI
from src.config.configLoad import load_config

client = OpenAI(
    api_key=load_config('OPENAI_API_KEY'),
    base_url=load_config('OPENAI_API_BASE')
)


def infer_llm(instruction, exemplars, query, model='gpt-3.5-turbo-0125', temperature=0.0, max_tokens=2048):
    messages = [
        # {"role": "system", "content": roleSystem},
        {"role": "user", "content": instruction},
        # {"role": "assistant", "content": roleAssistant},
    ]
    if exemplars is not None:
        for i, exemplar in enumerate(exemplars):
            messages.append({"role": "user", "content": exemplar['query']})
            messages.append(
                {"role": "assistant", "content": exemplar['answer']})
    if query is not None:
        messages.append({"role": "user", "content": query})

    retry_times = 0
    while retry_times < 3:
        try:
            answers = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                stream=False,
            )
            res = answers.choices[0].message.content
            return res
        except Exception as e:
            print("Exception :", e)
            if "list index out of range" in str(e):
                break
            retry_times += 1
    return "404ERROR"


def infer_llm_stream(instruction, exemplars, query, model='gpt-3.5-turbo-0125', temperature=0.0, max_tokens=2048):
    messages = [
        # {"role": "system", "content": roleSystem},
        {"role": "user", "content": instruction},
        # {"role": "assistant", "content": roleAssistant},
    ]
    try:
        answers = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True
        )

        # 处理流式响应
        for message in answers:
            if message.choices[0].delta.content is None:
                break
            yield message.choices[0].delta.content
    except Exception as e:
        print(f"LLM查询流发生错误: {e}")


if __name__ == '__main__':
    for i in infer_llm_stream("什么是日志", None, None):
        print(i)
    # print(infer_llm("什么是日志",None,None))
