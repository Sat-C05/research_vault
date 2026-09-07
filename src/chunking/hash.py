import hashlib

def generate_chunk_hash(text, algorithm = "sha256"):
    """Computes a cryptographic hash for a RAG text chunk."""
    hash_obj = hashlib.new(algorithm)
    # Encode string to bytes as required by hashlib
    hash_obj.update(text.encode("utf-8"))
    return hash_obj.hexdigest()

