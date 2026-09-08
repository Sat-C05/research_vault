from langchain_community.document_loaders import PyPDFLoader

def load_pdf(file_path):
    
    with open(file_path, "rb") as f:
        file_bytes = f.read()

    loader = PyPDFLoader(file_path)
    data = loader.load()

    return data, file_bytes
