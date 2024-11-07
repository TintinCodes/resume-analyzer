from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load and split the PDF document and return the documents and text chunks
def load_and_split_pdf(file_path):
    """
    load pdf and split pdf text
    """

    # loader
    loader = PyPDFLoader(file_path=file_path)
    documents = loader.load()

    # text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=20,
        separators=["\n\n", "\n", " ", ""],
    )
    chunks = text_splitter.split_documents(documents=documents)
    return documents, chunks
