import ollama

def generate_ans(question, context):
    prompt = f"""
    Answer the question using ONLY the provided context.

    If the context does not contain enough information to answer the question,
    say: "The provided documents do not contain enough information to answer this question."

    Do not use outside knowledge.
    Do not guess.
    Do not add information that is not supported by the context.

    Context:
    {context}

    Question:
    {question}
    """
    llm_response = ollama.chat(
    model='gemma2:2b',
    messages=[{'role': 'user', 'content': prompt}]
    )

    return llm_response