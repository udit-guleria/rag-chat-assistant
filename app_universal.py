import streamlit as st
import os
import shutil
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.document_loaders import (
    TextLoader, 
    PyPDFLoader, 
    Docx2txtLoader,
    CSVLoader,
    JSONLoader,
    UnstructuredHTMLLoader,
    UnstructuredMarkdownLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredPowerPointLoader,
    UnstructuredExcelLoader
)
import tempfile
import uuid
import mimetypes

# Load environment variables
load_dotenv()

# Configuration
CHROMA_PATH = "chroma"
UPLOAD_PATH = "data/uploads"
PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

# Supported file types and their loaders
SUPPORTED_TYPES = {
    # Text files
    'txt': TextLoader,
    'md': UnstructuredMarkdownLoader,
    'html': UnstructuredHTMLLoader,
    'htm': UnstructuredHTMLLoader,
    
    # Documents
    'pdf': PyPDFLoader,
    'docx': Docx2txtLoader,
    'doc': UnstructuredWordDocumentLoader,
    'ppt': UnstructuredPowerPointLoader,
    'pptx': UnstructuredPowerPointLoader,
    
    # Data files
    'csv': CSVLoader,
    'json': JSONLoader,
    'xlsx': UnstructuredExcelLoader,
    'xls': UnstructuredExcelLoader,
}

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'db' not in st.session_state:
    st.session_state.db = None
if 'uploaded_docs' not in st.session_state:
    st.session_state.uploaded_docs = []

def initialize_database():
    """Initialize the Chroma database"""
    try:
        embedding_function = OpenAIEmbeddings()
        if os.path.exists(CHROMA_PATH):
            db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
            return db
        return None
    except Exception as e:
        st.error(f"Error initializing database: {str(e)}")
        return None

def create_upload_directory():
    """Create upload directory if it doesn't exist"""
    os.makedirs(UPLOAD_PATH, exist_ok=True)

def get_file_extension(filename):
    """Get file extension from filename"""
    return Path(filename).suffix.lower().lstrip('.')

def process_uploaded_file(file_content, filename, file_type=None):
    """Process uploaded file and add to database"""
    try:
        file_ext = get_file_extension(filename)
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='wb', suffix=f'.{file_ext}', delete=False) as tmp_file:
            tmp_file.write(file_content)
            tmp_file_path = tmp_file.name
        
        # Choose the appropriate loader
        if file_ext in SUPPORTED_TYPES:
            loader_class = SUPPORTED_TYPES[file_ext]
            
            # Special handling for different file types
            if file_ext in ['csv', 'json']:
                loader = loader_class(tmp_file_path)
            else:
                loader = loader_class(tmp_file_path)
            
            # Load documents
            documents = loader.load()
            
            # Add metadata
            for doc in documents:
                doc.metadata['source'] = filename
                doc.metadata['upload_id'] = str(uuid.uuid4())
                doc.metadata['file_type'] = file_ext
            
            # Split text
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=300,
                chunk_overlap=100,
                length_function=len,
                add_start_index=True,
            )
            chunks = text_splitter.split_documents(documents)
            
            # Clean up temp file
            os.unlink(tmp_file_path)
            
            return chunks
        else:
            # Fallback to text loader for unsupported types
            st.warning(f"⚠️ Unsupported file type: {file_ext}. Attempting to read as text...")
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as tmp_file:
                try:
                    # Try to decode as text
                    text_content = file_content.decode('utf-8')
                    tmp_file.write(text_content)
                    tmp_file_path = tmp_file.name
                except UnicodeDecodeError:
                    st.error(f"❌ Cannot read {filename} as text. Please convert to a supported format.")
                    os.unlink(tmp_file_path)
                    return []
            
            loader = TextLoader(tmp_file_path, encoding='utf-8')
            documents = loader.load()
            
            for doc in documents:
                doc.metadata['source'] = filename
                doc.metadata['upload_id'] = str(uuid.uuid4())
                doc.metadata['file_type'] = 'txt_fallback'
            
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=300,
                chunk_overlap=100,
                length_function=len,
                add_start_index=True,
            )
            chunks = text_splitter.split_documents(documents)
            
            os.unlink(tmp_file_path)
            return chunks
            
    except Exception as e:
        st.error(f"Error processing file {filename}: {str(e)}")
        return []

def add_documents_to_database(chunks):
    """Add document chunks to the database"""
    try:
        embedding_function = OpenAIEmbeddings()
        
        if os.path.exists(CHROMA_PATH):
            # Load existing database
            db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
            # Add new documents
            db.add_documents(chunks)
        else:
            # Create new database
            db = Chroma.from_documents(
                chunks, embedding_function, persist_directory=CHROMA_PATH
            )
        
        return True
    except Exception as e:
        st.error(f"Error adding documents to database: {str(e)}")
        return False

def get_database_info():
    """Get information about documents in the database"""
    try:
        if not os.path.exists(CHROMA_PATH):
            return {"count": 0, "sources": [], "file_types": {}}
        
        embedding_function = OpenAIEmbeddings()
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
        
        # Get all documents
        all_docs = db.get()
        sources = set()
        file_types = {}
        
        for i, metadata in enumerate(all_docs.get('metadatas', [])):
            if 'source' in metadata:
                sources.add(metadata['source'])
                file_type = metadata.get('file_type', 'unknown')
                file_types[file_type] = file_types.get(file_type, 0) + 1
        
        return {
            "count": len(all_docs.get('ids', [])), 
            "sources": list(sources),
            "file_types": file_types
        }
    except Exception as e:
        st.error(f"Error getting database info: {str(e)}")
        return {"count": 0, "sources": [], "file_types": {}}

def query_database(question, db):
    """Query the database and return results"""
    try:
        # Search the database
        results = db.similarity_search_with_relevance_scores(question, k=3)
        
        if len(results) == 0 or results[0][1] < 0.7:
            return None, "Unable to find matching results. Please try rephrasing your question or upload more documents."
        
        # Prepare context
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        
        # Create prompt
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=question)
        
        # Get response from OpenAI
        model = ChatOpenAI()
        response_text = model.invoke(prompt).content
        
        # Get sources
        sources = [doc.metadata.get("source", "Unknown") for doc, _score in results]
        
        return response_text, sources
    except Exception as e:
        return None, f"Error processing query: {str(e)}"

def main():
    st.set_page_config(
        page_title="Universal Document RAG Assistant",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Header
    st.title("📚 Universal Document RAG Assistant")
    st.markdown("Upload documents in various formats and ask questions about them!")
    
    # Create upload directory
    create_upload_directory()
    
    # Sidebar
    with st.sidebar:
        st.header("📁 Document Management")
        
        # Supported file types info
        with st.expander("📋 Supported File Types"):
            st.markdown("""
            **Text Files:**
            - `.txt` - Plain text
            - `.md` - Markdown
            - `.html/.htm` - HTML files
            
            **Documents:**
            - `.pdf` - PDF documents
            - `.docx/.doc` - Word documents
            - `.ppt/.pptx` - PowerPoint presentations
            
            **Data Files:**
            - `.csv` - CSV spreadsheets
            - `.json` - JSON data
            - `.xlsx/.xls` - Excel spreadsheets
            """)
        
        # File upload
        uploaded_files = st.file_uploader(
            "Upload Documents",
            type=list(SUPPORTED_TYPES.keys()),
            accept_multiple_files=True,
            help="Upload documents in various formats to add to your knowledge base"
        )
        
        if uploaded_files:
            if st.button("📤 Process Uploaded Files", type="primary"):
                with st.spinner("Processing files..."):
                    total_chunks = 0
                    processed_files = 0
                    
                    for uploaded_file in uploaded_files:
                        file_content = uploaded_file.read()
                        chunks = process_uploaded_file(file_content, uploaded_file.name)
                        if chunks:
                            success = add_documents_to_database(chunks)
                            if success:
                                total_chunks += len(chunks)
                                processed_files += 1
                                st.session_state.uploaded_docs.append(uploaded_file.name)
                    
                    if total_chunks > 0:
                        st.success(f"✅ Successfully processed {processed_files}/{len(uploaded_files)} files with {total_chunks} chunks!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to process files")
        
        # Database info
        st.header("📊 Database Status")
        db_info = get_database_info()
        st.metric("Total Chunks", db_info["count"])
        
        if db_info["sources"]:
            st.write("**Documents in database:**")
            for source in db_info["sources"]:
                st.write(f"• {source}")
        
        if db_info["file_types"]:
            st.write("**File types:**")
            for file_type, count in db_info["file_types"].items():
                st.write(f"• {file_type}: {count} chunks")
        
        # Clear database button
        if st.button("🗑️ Clear Database", type="secondary"):
            if os.path.exists(CHROMA_PATH):
                shutil.rmtree(CHROMA_PATH)
                st.session_state.db = None
                st.session_state.uploaded_docs = []
                st.success("Database cleared!")
                st.rerun()
        
        # Example questions
        st.header("💡 Example Questions")
        example_questions = [
            "What is this document about?",
            "Summarize the main points",
            "What are the key concepts?",
            "Find information about [specific topic]",
            "What are the important details?"
        ]
        
        for question in example_questions:
            if st.button(question, key=f"example_{question}"):
                st.session_state.user_input = question
                st.rerun()
    
    # Main chat interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Show sources if available
                if message["role"] == "assistant" and "sources" in message:
                    with st.expander("📖 Sources"):
                        for i, source in enumerate(message["sources"], 1):
                            st.text(f"{i}. {source}")
    
    with col2:
        st.markdown("### 💡 Tips")
        st.markdown("""
        - Upload documents in various formats
        - Ask specific questions about your content
        - Use the example questions to get started
        - Each answer shows which documents were used
        - Supported: PDF, Word, PowerPoint, Excel, CSV, JSON, HTML, Markdown, Text
        """)
    
    # Check if database is initialized
    if st.session_state.db is None:
        with st.spinner("Initializing database..."):
            st.session_state.db = initialize_database()
    
    if st.session_state.db is None and db_info["count"] == 0:
        st.info("👆 Please upload some documents to get started!")
        st.stop()
    
    # Chat input
    if prompt := st.chat_input("Ask a question about your documents..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response, sources = query_database(prompt, st.session_state.db)
            
            if response:
                st.markdown(response)
                
                # Show sources
                if sources:
                    with st.expander("📖 Sources"):
                        for i, source in enumerate(sources, 1):
                            st.text(f"{i}. {source}")
                
                # Add assistant response to chat history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response,
                    "sources": sources
                })
            else:
                st.error(sources)  # sources contains error message in this case
    
    # Clear chat button
    if st.button("🗑️ Clear Chat", type="secondary"):
        st.session_state.messages = []
        st.rerun()

if __name__ == "__main__":
    main()
