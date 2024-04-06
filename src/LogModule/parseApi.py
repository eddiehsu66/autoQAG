import openai
from src.config.configLoad import load_config
openai.api_base, openai.api_key = load_config('OPENAI_API_BASE'), load_config('OPENAI_API_KEY')


def infer_llm(instruction, exemplars, query, log_message, model='gpt-3.5-turbo', temperature=0.0, max_tokens=2048):

    messages = [
        {"role": "system", "content": "You are an expert of log parsing, and now you will help to do log parsing."},
        {"role": "user", "content": instruction},
        {"role": "assistant", "content": "Sure, I can help you with log parsing."},
    ]

    if exemplars is not None:
        for i, exemplar in enumerate(exemplars):
            messages.append({"role": "user", "content": exemplar['query']})
            messages.append(
                {"role": "assistant", "content": exemplar['answer']})
    messages.append({"role": "user", "content": query})
    # my_json = json.dumps(messages, ensure_ascii=False, separators=(',', ':'))
    # print(my_json)
    retry_times = 0
    while retry_times < 3:
        try:
            answers = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=temperature,
                stream=False,
                # frequency_penalty=0.0,
                # presence_penalty=0.0,
            )
            return [response["message"]["content"] for response in answers["choices"] if
                    response['finish_reason'] != 'length'][0]
        except Exception as e:
            print("Exception :", e)
            if "list index out of range" in str(e):
                break
            # print(answers)
            retry_times += 1
    print(f"Failed to get response from OpenAI after {retry_times} retries.")
    if exemplars is not None and len(exemplars) > 0:
        if exemplars[0]['query'] != 'Log message: `try to connected to host: 172.16.254.1, finished.`' \
                or exemplars[0]['answer'] != 'Log template: `try to connected to host: {ip_address}, finished.`':
            examples = [{'query': 'Log message: `try to connected to host: 172.16.254.1, finished.`',
                         'answer': 'Log template: `try to connected to host: {ip_address}, finished.`'}]
            return infer_llm(instruction, examples, query, log_message, model, temperature, max_tokens)
    return 'Log message: `{}`'.format(log_message)


if __name__ == '__main__':
    for i in range(100):
        log = "WindowManager: startAnimation end"
        print(infer_llm(
            "I want you to act like an expert of log parsing. I will give you a log message delimited by backticks. You must identify and abstract all the dynamic variables in logs with {placeholder} and output a static log template. Print the input log's template delimited by backticks."
            , None
            , 'Log message: `{}`'.format(log)
            , log))




def get_response_from_openai_key(query, examples=[], model='gpt-3.5-turbo-0613', temperature=0.0):
    # Prompt-1
    # instruction = "I want you to act like an expert of log parsing. I will give you a log message enclosed in backticks. You must identify and abstract all the dynamic variables in logs with {placeholder} and output a static log template. Print the input log's template enclosed in backticks."
    instruction = "I want you to act like an expert of log parsing. I will give you a log message delimited by backticks. You must identify and abstract all the dynamic variables in logs with {placeholder} and output a static log template. Print the input log's template delimited by backticks."
    if examples is None or len(examples) == 0:
        examples = [{'query': 'Log message: `try to connected to host: 172.16.254.1, finished.`',
                     'answer': 'Log template: `try to connected to host: {ip_address}, finished.`'}]
    question = 'Log message: `{}`'.format(query)
    responses = infer_llm(instruction, examples, question, query,
                          model, temperature, max_tokens=2048)
    return responses


def query_template_from_gpt(log_message, examples=[], model='gpt-3.5-turbo-0613'):
    if len(log_message.split()) == 1:
        return log_message, False
    # print("prompt base: ", prompt_base)
    response = get_response_from_openai_key(log_message, examples, model)
    # print(response)
    lines = response.split('\n')
    log_template = None
    for line in lines:
        if line.find("Log template:") != -1:
            log_template = line
            break
    if log_template is None:
        for line in lines:
            if line.find("`") != -1:
                log_template = line
                break
    if log_template is not None:
        start_index = log_template.find('`') + 1
        end_index = log_template.rfind('`')

        if start_index == 0 or end_index == -1:
            start_index = log_template.find('"') + 1
            end_index = log_template.rfind('"')

        if start_index != 0 and end_index != -1 and start_index < end_index:
            template = log_template[start_index:end_index]
            return template, True

    print("======================================")
    print("ChatGPT response format error: ")
    print(response)
    print("======================================")
    return log_message, False
