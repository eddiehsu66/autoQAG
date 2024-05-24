from qdrant_client import QdrantClient,models
from src.config.configLoad import load_config


def qdrant_init():
    return QdrantClient(
        load_config('Qdrant')['url'],
        api_key=load_config('Qdrant')['apiKey'],
    )


if __name__ == '__main__':
    client = qdrant_init()
    # client.create_collection(
    #     collection_name="example_collection",
    #     vectors_config=models.VectorParams(size=4, distance=models.Distance.DOT)
    # )
    # print("Collection created.")

    points = [
        models.PointStruct(id=1, vector=[0.1, 0.2, 0.3, 0.4], payload={"name": "item1"}),
        models.PointStruct(id=2, vector=[0.4, 0.3, 0.2, 0.1], payload={"name": "item2"}),
    ]
    client.upsert(
        collection_name="example_collection",
        points=points
    )
    print("Vectors inserted.")

    search_result = client.search(
        collection_name="example_collection",
        query_vector=[0.15, 0.25, 0.35, 0.45],
        limit=2
    )
    print("Search results:", search_result)