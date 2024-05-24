from llama_index.core import Document, SimpleDirectoryReader
from llama_index.core.schema import MetadataMode
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.extractors import TitleExtractor, QuestionsAnsweredExtractor
from llama_index.core.ingestion import IngestionPipeline
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.qdrant import QdrantVectorStore

from src.config.configLoad import load_config
from src.config.qdrantKit import qdrant_init

# 数据和模型路径
target_files = [
    "../../cache/documents/test.txt",
]
MODEL_NAME = "WhereIsAI/UAE-Large-V1"


def documentToVector():
    documents = SimpleDirectoryReader(input_files=target_files).load_data()
    vector_store = QdrantVectorStore(client=qdrant_init(), collection_name="test_store")
    llm = OpenAI(model="gpt-3.5-turbo-0125", temperature=0.1, api_key=load_config('OPENAI_API_KEY'),
                 api_base=load_config('OPENAI_API_BASE'))
    qa_extractor = QuestionsAnsweredExtractor(questions=3)
    pipeline = IngestionPipeline(
        transformations=[
            SentenceSplitter(chunk_size=256, chunk_overlap=32),
            TitleExtractor(
                llm=llm, metadata_mode=MetadataMode.EMBED, num_workers=8
            ),
            HuggingFaceEmbedding(model_name=MODEL_NAME)
        ],
        vector_store=vector_store,
    )
    pipeline.run(documents=documents)


if __name__ == '__main__':
    documentToVector()
