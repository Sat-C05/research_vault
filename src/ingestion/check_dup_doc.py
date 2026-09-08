from scripts.hash_fucntions import hash_bytes

def check_document(file_bytes, filename, collection):
    
    document_hash = hash_bytes(file_bytes)

    existing_docs = collection.get(
        where={"document_hash": document_hash}
    )

    if existing_docs and len(existing_docs["ids"]) > 0:
        print(f"Document already exists: {filename}")
        return {"status": "duplicate", "document_hash": document_hash}

    return {"status": "new", "document_hash": document_hash}
