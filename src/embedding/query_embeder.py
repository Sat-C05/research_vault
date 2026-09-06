from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

def embed_query(query):
    embedding_function = SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
    )

    response = embedding_function([query])
    query_vector = response[0]
    
    return query_vector