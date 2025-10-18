# Simple version that bypasses the unstructured library issues
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import os
import shutil

# Load environment variables
load_dotenv()

CHROMA_PATH = "chroma"
DATA_PATH = "data/books"

def main():
    generate_data_store()

def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)

def load_documents():
    # Use TextLoader instead of DirectoryLoader to avoid unstructured issues
    documents = []
    for filename in os.listdir(DATA_PATH):
        if filename.endswith('.md'):
            file_path = os.path.join(DATA_PATH, filename)
            loader = TextLoader(file_path, encoding='utf-8')
            docs = loader.load()
            documents.extend(docs)
    return documents

def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    if len(chunks) > 10:
        document = chunks[10]
        print(document.page_content)
        print(document.metadata)

    return chunks

def save_to_chroma(chunks: list[Document]):
    # Clear out the database first.
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # Create a new DB from the documents.
    try:
        embedding_function = OpenAIEmbeddings()
        db = Chroma.from_documents(
            chunks, embedding_function, persist_directory=CHROMA_PATH
        )
        db.persist()
        print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")
    except Exception as e:
        print(f"Error creating database: {e}")
        print("This might be due to OpenAI API key not being set or network issues.")

if __name__ == "__main__":
    main()

