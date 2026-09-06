from src.chunking.splitter import split_doc
from src.ingestion.loader import load_pdf
from src.embedding.embedding import embed_documents
from src.retrieval.retrival import retrival
from src.generation.generate_ans import generate_ans
from src.embedding.query_embeder import embed_query

data = load_pdf("data/inorganic_chemistry1.pdf")
chunks = split_doc(data)

embeded_collection = embed_documents(chunks)

query = input("Enter your question: ")

query_vector = embed_query(query)

context = retrival(query_vector, embeded_collection)

response = generate_ans(query, context)

print(response['message']['content'])
