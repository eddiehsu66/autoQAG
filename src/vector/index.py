from llama_index.core import Settings, VectorStoreIndex, StorageContext
from llama_index.core.readers import SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.faiss import FaissVectorStore
import faiss

# 数据和模型路径
DATA_PATH = "./data"
MODEL_NAME = "bert-base-uncased"

# 加载数据
documents = SimpleDirectoryReader(DATA_PATH, filename_as_id=True).load_data()

# 创建嵌入模型和LLM
embed_model = HuggingFaceEmbedding(model_name=MODEL_NAME)

# 配置全局设置
Settings.embed_model = embed_model

# 创建Faiss向量存储
dimension = 768  # 假设使用的BERT模型的向量维度为768
faiss_index = faiss.IndexFlatL2(dimension)
vector_store = FaissVectorStore(faiss_index=faiss_index)

# 创建存储上下文
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# 构建向量索引
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context
)

# 查询向量索引
query_engine = index.as_query_engine()
response = query_engine.query("查询内容")
print(response)