import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

def embed_documents(chunks):
    embedding_function = SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
    )

    client = chromadb.PersistentClient(path="data/my_chroma_db_research_vault")


    collection = client.get_or_create_collection(
        name="inorganic_chemistry_collection",
        embedding_function=embedding_function
    )


    collection.add(
        documents=[chunk.page_content for chunk in chunks],
        metadatas=[chunk.metadata for chunk in chunks],
        ids=[f"chunk_{i}" for i in range(len(chunks))]
    )

    return collection