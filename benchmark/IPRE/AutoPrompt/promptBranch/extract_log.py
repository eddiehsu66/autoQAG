import re

import pandas as pd

from benchmark.IPRE.AutoPrompt.promptApi import infer_llm
import concurrent.futures

from benchmark.IPRE.AutoPrompt.selectLog import get_train_dataSet
from src.config.configLoad import load_config
from src.config.redisKit import redisInit
from src.config.configLoad import load_config
name = load_config('BaseObject')

def TaskExtractLog(entityA, entityB, context, prompt, real_relation):
    listName = ''
    result_item = []
    if name == 'teacher':
        listName = '1、老师 2、学生 3、其他'
    elif name == 'brother':
        listName = '1、哥哥 2、弟弟 3、姐姐 4、妹妹 5、其他'
    elif name == 'couple':
        listName = '1、现夫 2、前夫 3、未婚夫 4、现妻 5、前妻 6、未婚妻 7、其他'
    else:
        exit(404)

    prompt_temp = ("You will be provided with two entities and context"
                   f"{prompt}"
                   f"EntityA:<START>{entityA}<END>"
                   f"EntityB:<START>{entityB}<END>"
                   f"Context:<START>{context}<END>"
                   f"Output the relation EntityA relative to EntityB "
                   f"in <LIST> {listName} </LIST> base on Context\n"
                   f"Please follow the example below to identify relation: \n" + select_log(3))
    # client = redisInit()
    # if client.get(prompt_temp) is not None:
    #     response = client.get(prompt_temp)
    # else:
    #     response = infer_llm(prompt_temp, None, None, cached=False)
    response = infer_llm(prompt_temp, None, None, cached=False)
    if response != "404ERROR":
        relationA = limit_word(real_relation)
        relationB = limit_word(parse_response(response))
        # if relationA == relationB:
        #     client.set(prompt_temp,response)
        result_item.append(entityA)
        result_item.append(entityB)
        result_item.append(context.replace(' ', ''))
        result_item.append(prompt)
        result_item.append(relationA)
        result_item.append(relationB)
        # print(result_item)
    return result_item


def extract_log_template(prompts,mode='train'):
    if mode == 'train':
        path = f"C:/code/src/python/autoQAG/data/ipre_data/train/train_{name}.csv"
    else:
        path = f"C:/code/src/python/autoQAG/data/ipre_data/test/test_{name}.csv"
    df = pd.read_csv(path, header=None)
    result = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=load_config("ThreadNum")) as executor:
        futures = []
        for index, raw in df.iterrows():
            entityA = raw[0]
            entityB = raw[1]
            context = raw[2].replace(' ', '')
            relation = raw[3]
            for prompt in prompts:
                future = executor.submit(TaskExtractLog, entityA, entityB, context, prompt, relation)
                futures.append(future)
        for future in concurrent.futures.as_completed(futures):
            if len(future.result()) != 0:
                result.append(future.result())
    return result


def select_log(num: int):
    pd = get_train_dataSet()
    new_pd = pd.sample(n=num)
    text = "This is example:\n"
    for _, row in new_pd.iterrows():
        text += "<Example>" + (f"Entity: <START>{row[0]}<END>\n"
                               f"Entity: <START>{row[1]}<END>\n"
                               f"Context: <START>{row[2]}<END>\n"
                               f"Relation: <START>{row[3]}<END>\n") + "</Example>"
    return text


def parse_response(log):
    match = re.search(r'(?<=Relation: <START>).*', log)
    if match:
        content = match.group(0)
        return content.replace("\n", "").replace("<END>", "").replace("<START>", "")
    return log.replace("\n", "").replace("<END>", "").replace("<START>", "")


def limit_word(text):
    keywords = []
    if name == 'teacher':
        keywords = ['老师','学生','其他']
    elif name == 'brother':
        keywords = ['哥哥','弟弟','姐姐','妹妹','其他']
    elif name == 'couple':
        keywords = ['现夫','前夫','未婚夫','现妻','前妻','未婚妻','其他']
    else:
        exit(404)
    for keyword in keywords:
        if keyword in text:
            return keyword
    return '其他'


if __name__ == '__main__':
    print(TaskExtractLog("韩小莹", "郭靖",
                         "越女剑 法 — — 这 “ 越女剑 法 ” 乃 当年 江南七怪 中 的 韩小莹 传 与 郭靖 ， 其后 韩小莹 不幸 惨死 ， 郭靖感 念 师恩 ， 珍而重 之 的 传 了 给 两个 "
                         "女儿 。",
                         "'The process of identifying the relationship between entities based on a given context "
                         "involves extracting the names of the entities mentioned (EntityA and EntityB), "
                         "analyzing the surrounding text to understand how they are related, and determining the type "
                         "of relationship they have (such as family relation, professional relation, etc). This "
                         "process helps language model assistants improve the accuracy of identifying relations "
                         "between entities in various contexts.", "学生"))
    # print(parse_log('Relation: <START>老师<END>\n xxxxxxx'))
