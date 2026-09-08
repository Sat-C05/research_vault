import time

from src.chunking.splitter import split_doc
from src.ingestion.loader import load_pdf
from src.embedding.embedding import embed_documents, get_collection
from src.ingestion.check_dup_doc import check_document
from src.retrieval.retrival import retrival
from src.generation.generate_ans import generate_ans
from src.embedding.query_embeder import embed_query


def main():

    filename = "data/imorganic_chemistry_para_changed.pdf"

    data, file_bytes = load_pdf(filename)
    collection = get_collection()

    result = check_document(file_bytes, filename, collection)

    if result["status"] == "duplicate":
        query = input("Enter your question: ")

        query_vector = embed_query(query)

        context = retrival(query_vector, collection)

        response = generate_ans(query, context)

        print(response['message']['content'])

    else:

        chunks = split_doc(data, collection, result["document_hash"], filename)

        embeded_collection = embed_documents(chunks, collection) if chunks else collection

        query = input("Enter your question: ")

        query_vector = embed_query(query)

        context = retrival(query_vector, embeded_collection)

        response = generate_ans(query, context)

        print(response['message']['content'])

if __name__ == "__main__":
    start = time.perf_counter()
    main()
    elapsed = time.perf_counter() - start
    print(f"Total run time: {elapsed:.2f}s")