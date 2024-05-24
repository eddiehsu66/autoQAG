import json
import re

import pandas as pd
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from src.config.openaiKit import infer_llm


def question_extractor(context_str, num_questions):
    prompt = (f'Here is the context:{context_str} '
              f'Given the contextual information,'
              f'generate {num_questions} questions '
              f'this context can provide specific answers to which are unlikely to be found elsewhere.Higher-level '
              f'summaries of surrounding context may be provided as well. Try using these summaries to generate '
              f'better questions that this context can answer.')
    return infer_llm(prompt, None, None)


def answer_extractor(context_question, context_str):
    prompt = (f'Here is the context:{context_str}'
              f'Here is the question:{context_question} '
              f'Given the contextual context,'
              f'generate specific answers to the question. ')
    return infer_llm(prompt, None, None)


def question_answer_pair(context, num_questions=5):
    qapList = []
    questions = question_extractor(context, num_questions).split('\n')
    for question in questions:
        pattern = r'^\d+\.\s*'
        question = re.sub(pattern, '', question)
        answer = answer_extractor(question, context)
        qapList.append((context, question, answer))
    return qapList


if __name__ == '__main__':
    uuid_id = 'def865f9-571e-4011-aa9c-70a77e979ed6'
    process_path = f'../../cache/logs/{uuid_id}/process_set.csv'
    df = pd.read_csv(process_path)
    context_list = df.iloc[:, 0].tolist()
    MODEL_NAME = "WhereIsAI/UAE-Large-V1"
    embed_model = HuggingFaceEmbedding(model_name=MODEL_NAME)
    points = []
    for context in context_list:
        qapList = question_answer_pair(context)
        for qap in qapList:
            question = qap[1]
            answer = qap[2]
            context = qap[0]
            embedding = embed_model.get_text_embedding(question)
            points.append({"question": question, "answer": answer, "content": context,"embedding": embedding})
    points_json = json.dumps(points, ensure_ascii=False, indent=4)
    print(points_json)
