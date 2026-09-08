import hashlib


def hash_bytes(data):
    """
    SHA-256 hash for raw file/document bytes.
    Used for document-level deduplication.
    """
    return hashlib.sha256(data).hexdigest()


def hash_text(text):
    """
    SHA-256 hash for text.
    Used for chunk-level deduplication.
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
