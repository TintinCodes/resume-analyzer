from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

def create_vector_store(chunks):
    """
    Store embeddings of all the chunks into a vector store
    """
    print(f"length of chunks:{len(chunks)}")

    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )
    print(f"vector store:{vector_store}")
    return vector_store
