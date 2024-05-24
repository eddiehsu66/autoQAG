import re

from llama_index.core import Document, SimpleDirectoryReader
from llama_index.core.schema import MetadataMode
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.extractors import TitleExtractor
from llama_index.core.ingestion import IngestionPipeline
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.readers.file import CSVReader
from llama_index.core.extractors import QuestionsAnsweredExtractor

from src.LogModule.questionAnswerExtractor import question_answer_pair
from src.config.configLoad import load_config
from src.config.qdrantKit import qdrant_init
import pandas as pd
from src.config.openaiKit import infer_llm
import uuid
from qdrant_client import QdrantClient, models

MODEL_NAME = "WhereIsAI/UAE-Large-V1"


def logToVector(id: str):
    target_files = [
        f'../../cache/logs/{id}/Test_template.csv'
    ]
    parser = CSVReader()
    file_extractor = {".csv": parser}  # Add other CSV formats as needed

    documents = SimpleDirectoryReader(
        input_files=target_files, file_extractor=file_extractor
    ).load_data()
    llm = OpenAI(model="gpt-3.5-turbo-0125", temperature=0.1, api_key=load_config('OPENAI_API_KEY'),
                 api_base=load_config('OPENAI_API_BASE'))

    vector_store = QdrantVectorStore(client=qdrant_init(), collection_name=id)
    questions_answered_extractor = QuestionsAnsweredExtractor(llm=llm, questions=3)
    pipeline = IngestionPipeline(
        transformations=[
            SentenceSplitter(chunk_size=60, chunk_overlap=10),
            TitleExtractor(
                llm=llm, metadata_mode=MetadataMode.EMBED, num_workers=8
            ),
            questions_answered_extractor,
            HuggingFaceEmbedding(model_name=MODEL_NAME)
        ],
        vector_store=vector_store,
    )
    pipeline.run(documents=documents, in_place=True, show_progress=True)


def simple_qa_worker(content, predecessor, successor):
    prompt_temp = (f"you can cook some question and answer from various angles based provided with a log context and "
                   f"its predecessor and"
                   f"its successor without any superfluous output"
                   f"log context:{content}"
                   f"predecessor:{predecessor}"
                   f"successor:{successor}"
                   f"your mother would be proud of you if you can make it correctly")
    example = ("here some example of make question and answer\n"
               "<QUESTION>What is the current status of the updateDimmedActivatedHideSensitive feature?</QUESTION> "
               "<ANSWER>The current status is overlap:false.</ANSWER>"
               "<QUESTION>Can you provide an update on the progress of the new feature implementation?</QUESTION> "
               "<ANSWER>The new feature implementation is currently in the testing phase.</ANSWER>"
               "<QUESTION>What log message is being output when trying to register a callback not in the UI?</QUESTION> "
               "<ANSWER>Sorry,I don't know,It is superfluous output</ANSWER>"
               )
    return infer_llm(prompt_temp + example, None, None)


def row_worker(uuid_id, row):
    content = row['Content']
    predecessor = row['predecessor']
    successor = row['successor']
    qaList = llm_parse(simple_qa_worker(content, predecessor, successor))

    embed_model = HuggingFaceEmbedding(model_name=MODEL_NAME)
    client = qdrant_init()
    points = []
    collection_name = uuid_id
    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=1024, distance=models.Distance.DOT)
        )
        print("Collection created.")
    for qa in qaList:
        question = qa['question']
        answer = qa['answer']
        question_embedding = embed_model.get_text_embedding(question)
        points.append(models.PointStruct(
            id=str(uuid.uuid4()),
            vector=question_embedding,
            payload={"question": question, "answer": answer, "content": content}
        ))
        client.upsert(
            collection_name=uuid_id,
            points=points
        )


def llm_parse(input_string):
    pattern = re.compile(r'<QUESTION>(.*?)</QUESTION>\s*<ANSWER>(.*?)</ANSWER>', re.DOTALL)
    matches = pattern.findall(input_string)
    parsed_data = []
    for match in matches:
        question, answer = match
        if 'sorry' not in answer.strip().lower():
            parsed_data.append({
                'question': question.strip(),
                'answer': answer.strip()
            })
    return parsed_data


@DeprecationWarning
def make_qa_embedding(uuid_id):
    process_path = f'../../cache/logs/{uuid_id}/Test_process.csv'
    df = pd.read_csv(process_path)
    df.apply(lambda row: row_worker(uuid_id, row), axis=1)


def question_answer_embedding(uuid_id):
    process_path = f'../../cache/logs/{uuid_id}/process_set.csv'
    df = pd.read_csv(process_path)
    context_list = df.iloc[:, 0].tolist()
    embed_model = HuggingFaceEmbedding(model_name=MODEL_NAME)
    client = qdrant_init()
    points = []
    collection_name = uuid_id
    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=1024, distance=models.Distance.DOT)
        )
        print(f"{uuid_id} Collection created.")
    for context in context_list:
        qapList = question_answer_pair(context)
        for qap in qapList:
            question = qap[1]
            answer = qap[2]
            context = qap[0]
            question_embedding = embed_model.get_text_embedding(question)
            points.append(models.PointStruct(
                id=str(uuid.uuid4()),
                vector=question_embedding,
                payload={"question": question, "answer": answer, "content": context}
            ))
    client.upsert(
        collection_name = uuid_id,
        points = points
    )

if __name__ == '__main__':
    question_answer_embedding('def865f9-571e-4011-aa9c-70a77e979ed6')
