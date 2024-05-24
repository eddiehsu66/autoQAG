from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.core.indices.vector_store import VectorIndexAutoRetriever
from llama_index.core.vector_stores.types import VectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.qdrant import QdrantVectorStore

from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.qdrant import QdrantVectorStore
from src.config.configLoad import load_config
from src.config.qdrantKit import qdrant_init
from src.server.entity.history import get_chatHistoy_by_uuid

MODEL_NAME = "WhereIsAI/UAE-Large-V1"


def log_retriever(uuid, query_text):
    # vector_store = QdrantVectorStore(client=qdrant_init(), collection_name=uuid)
    # llm = OpenAI(model="gpt-3.5-turbo-0125", temperature=0.1, api_key=load_config('OPENAI_API_KEY'))
    # storage_context = StorageContext.from_defaults(vector_store=vector_store)
    #
    # index = VectorStoreIndex.from_vector_store(
    #     vector_store=vector_store,
    #     embed_model = HuggingFaceEmbedding(model_name=MODEL_NAME)
    # )
    # query_engine = index.as_query_engine(llm=llm)
    # response = query_engine.aquery(
    #     "What baseline models are measured against in the paper?"
    # )
    #
    # print(response)
    embed_model = HuggingFaceEmbedding(model_name=MODEL_NAME)
    embedding = embed_model.get_text_embedding(query_text)
    client = qdrant_init()
    search_result = client.search(
        collection_name='def865f9-571e-4011-aa9c-70a77e979ed6',
        query_vector=embedding,
        limit=5
    )
    rel_work = "This is the content that is relevant to you, and the relevance is in descending order. \n"
    for res in search_result:
        rel_work += str(res.payload) + '\n'
    return rel_work


def chat_prompt(uuid, query_text):
    relevant_work = log_retriever(uuid, query_text)
    history_context = str(get_chatHistoy_by_uuid(uuid))
    prompt = (f"you are a chatbot, and you are chatting with a user. The user is asking you a question.you can answer "
              f"base on the relevant work and history_context \n"
              f"<Relevant_work>{relevant_work}</Relevant_work>\n"
              f"<History_context>{history_context}</History_context>\n"
              f"response in Chinese\n")
    return prompt

if __name__ == '__main__':
    chat_prompt('8F5B632B-B127-5294-DB7F-277AD406D193')
