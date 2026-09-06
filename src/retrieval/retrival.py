def retrival(query_vector, collection):

    
    results = collection.query(
    query_embeddings=[query_vector],
    n_results=3
    )

    retrieved_texts = results['documents'][0]
    context = "\n\n".join(retrieved_texts)
    return context