from langchain_text_splitters import RecursiveCharacterTextSplitter
from scripts.hash_fucntions import hash_text


def split_doc(data, collection, document_hash, filename):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(data)

    new_chunks = []
    current_hashes = set()

    for index, chunk in enumerate(chunks):

        chunk_hash = hash_text(chunk.page_content)
        current_hashes.add(chunk_hash)

        existing = collection.get(
            ids=[chunk_hash]
        )

        if existing["ids"]:
            print(f"Duplicate chunk found: {chunk_hash}")
            continue

        chunk.metadata["chunk_hash"] = chunk_hash
        chunk.metadata["chunk_index"] = index
        chunk.metadata["document_hash"] = document_hash
        chunk.metadata["filename"] = filename

        new_chunks.append(chunk)

    # Any chunk previously stored for this filename that isn't part of the
    # current version of the file belongs to an old, edited-away version —
    # remove it so retrieval doesn't surface stale content.
    previous_chunks = collection.get(where={"filename": filename})
    stale_ids = [
        chunk_id for chunk_id in previous_chunks["ids"]
        if chunk_id not in current_hashes
    ]

    if stale_ids:
        print(f"Removing {len(stale_ids)} stale chunk(s) for {filename}")
        collection.delete(ids=stale_ids)

    return new_chunks