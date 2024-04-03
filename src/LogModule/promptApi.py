import openai

from src.QaMaker.configLoad import load_config
openai.api_base, openai.api_key = load_config('OPENAI_API_BASE'), load_config('OPENAI_API_KEY')


def infer_llm(instruction, exemplars, query,model='gpt-3.5-turbo', temperature=0.0, max_tokens=2048,logger=None):

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
            answers = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=temperature,
                stream=False,
            )
            return [response["message"]["content"] for response in answers["choices"] if
                    response['finish_reason'] != 'length'][0]
        except Exception as e:
            if logger is not None:
                logger.info("Exception : {}".format(e))
            else:
                print("Exception :", e)
            if "list index out of range" in str(e):
                break
            retry_times += 1
    if exemplars is not None and len(exemplars) > 0:
        if exemplars[0]['query'] != 'Log message: `try to connected to host: 172.16.254.1, finished.`' \
                or exemplars[0]['answer'] != 'Log template: `try to connected to host: {ip_address}, finished.`':
            examples = [{'query': 'Log message: `try to connected to host: 172.16.254.1, finished.`',
                         'answer': 'Log template: `try to connected to host: {ip_address}, finished.`'}]
            return infer_llm(instruction,exemplars,query)
        if logger is not None:
            logger.error(f"Failed to get response from OpenAI after {retry_times} retries.")
        else:
            print(f"Failed to get response from OpenAI after {retry_times} retries.")
    return "Failed to get response from OpenAI after {} retries.".format(retry_times)