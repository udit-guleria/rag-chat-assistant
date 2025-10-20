# 🛠️ Developer Guide - Universal Document RAG Assistant

## 🚀 Quick Start for Developers

### Prerequisites
```bash
# Python 3.8+
python --version

# Git
git --version

# OpenAI API Key
# Get from: https://platform.openai.com/api-keys
```

### Development Setup
```bash
# 1. Clone repository
git clone https://github.com/udit-guleria/rag-chat-assistant.git
cd rag-chat-assistant

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# OR
.venv\Scripts\activate      # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment
echo "OPENAI_API_KEY=your_key_here" > .env

# 5. Run development server
python run_ui.py
```

## 🏗️ Architecture Overview

### Core Files
```
app.py                    # Main Streamlit application
├── initialize_database() # Database setup
├── process_uploaded_file() # File processing
├── add_documents_to_database() # Database operations
├── query_database()      # Query processing
└── main()               # UI and interaction

run_ui.py                # Application launcher
├── check_database()     # Database validation
└── main()               # Launch logic

document_manager.py       # CLI management tool
├── get_database_info() # Database statistics
├── clear_database()     # Database cleanup
└── search_documents()   # Document search
```

### Data Flow
```
User Upload → File Processing → Text Chunking → Embeddings → Vector DB
                                                                    ↓
User Query → Semantic Search → Context Retrieval → AI Generation → Response
```

## 🔧 Key Components

### 1. Document Processing Pipeline

```python
# File Upload & Processing
def process_uploaded_file(file_content, filename, file_type=None):
    # 1. Create temporary file
    # 2. Choose appropriate loader
    # 3. Extract text content
    # 4. Add metadata
    # 5. Split into chunks
    # 6. Return processed chunks
```

### 2. Vector Database Operations

```python
# Database Management
def add_documents_to_database(chunks):
    # 1. Initialize embeddings
    # 2. Load existing database
    # 3. Add new documents
    # 4. Persist changes

def query_database(question, db):
    # 1. Semantic search
    # 2. Relevance filtering
    # 3. Context preparation
    # 4. AI generation
    # 5. Source attribution
```

### 3. Supported File Types

```python
SUPPORTED_TYPES = {
    # Text files
    'txt': TextLoader,
    'md': UnstructuredMarkdownLoader,
    'html': UnstructuredHTMLLoader,
    
    # Documents
    'pdf': PyPDFLoader,
    'docx': Docx2txtLoader,
    'ppt': UnstructuredPowerPointLoader,
    
    # Data files
    'csv': CSVLoader,
    'json': JSONLoader,
    'xlsx': UnstructuredExcelLoader,
}
```

## 🧪 Testing

### Unit Testing
```bash
# Create test file
touch test_app.py

# Run tests
python -m pytest test_app.py -v
```

### Manual Testing
```bash
# 1. Test file upload
python run_ui.py
# Upload different file types
# Verify processing works

# 2. Test queries
python query_data.py "Test question"
# Verify responses are relevant

# 3. Test database management
python document_manager.py
# Test all CLI options
```

### Integration Testing
```bash
# Test complete workflow
python create_database_simple.py  # Create sample data
python run_ui.py                 # Launch interface
# Test upload, query, and management features
```

## 🔍 Debugging

### Common Debug Scenarios

#### 1. File Upload Issues
```python
# Add debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Check file processing
def process_uploaded_file(file_content, filename, file_type=None):
    print(f"Processing file: {filename}")
    print(f"File size: {len(file_content)} bytes")
    print(f"File type: {file_type}")
    # ... rest of function
```

#### 2. Database Issues
```python
# Check database status
def debug_database():
    if os.path.exists(CHROMA_PATH):
        print("Database exists")
        # Check database contents
        db_info = get_database_info()
        print(f"Database info: {db_info}")
    else:
        print("Database not found")
```

#### 3. Query Issues
```python
# Debug query processing
def debug_query(question, db):
    print(f"Query: {question}")
    results = db.similarity_search_with_relevance_scores(question, k=3)
    print(f"Results count: {len(results)}")
    for i, (doc, score) in enumerate(results):
        print(f"Result {i}: Score={score}, Source={doc.metadata.get('source')}")
```

### Logging Configuration
```python
# Add to app.py
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

## 🚀 Performance Optimization

### Database Optimization
```python
# Optimize chunking strategy
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,      # Smaller = more precise
    chunk_overlap=100,   # Higher = more context
    length_function=len,
    add_start_index=True,
)

# Optimize search parameters
results = db.similarity_search_with_relevance_scores(
    query, 
    k=3,  # Number of results
    score_threshold=0.7  # Relevance threshold
)
```

### Memory Optimization
```python
# Process large files in batches
def process_large_file(file_content, filename):
    # Split file into smaller chunks
    chunk_size = 1024 * 1024  # 1MB chunks
    for i in range(0, len(file_content), chunk_size):
        chunk = file_content[i:i + chunk_size]
        process_chunk(chunk, f"{filename}_part_{i//chunk_size}")
```

## 🔧 Customization

### Adding New File Formats
```python
# 1. Add to SUPPORTED_TYPES
SUPPORTED_TYPES['new_format'] = NewFormatLoader

# 2. Handle special cases
if file_ext == 'new_format':
    # Special processing for new format
    loader = NewFormatLoader(tmp_file_path, special_param=True)
```

### Custom Chunking Strategy
```python
# Custom text splitter
class CustomTextSplitter(RecursiveCharacterTextSplitter):
    def __init__(self):
        super().__init__(
            chunk_size=500,
            chunk_overlap=150,
            length_function=len,
            add_start_index=True,
        )
    
    def split_text(self, text):
        # Custom splitting logic
        return super().split_text(text)
```

### Custom Embeddings
```python
# Use different embedding model
from langchain.embeddings import HuggingFaceEmbeddings

embedding_function = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
```

## 📦 Deployment

### Local Development
```bash
# Development mode with auto-reload
streamlit run app.py --server.runOnSave true
```

### Production Deployment
```bash
# Production mode
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 🔒 Security

### API Key Management
```python
# Secure API key handling
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get('OPENAI_API_KEY')

if not api_key:
    raise ValueError("OpenAI API key not found")
```

### Input Validation
```python
# Validate file uploads
def validate_file(file):
    # Check file size
    if file.size > 200 * 1024 * 1024:  # 200MB limit
        raise ValueError("File too large")
    
    # Check file type
    if file.type not in ALLOWED_TYPES:
        raise ValueError("Unsupported file type")
    
    return True
```

## 📊 Monitoring

### Application Metrics
```python
# Add metrics collection
import time
from functools import wraps

def track_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.2f} seconds")
        return result
    return wrapper

@track_performance
def process_uploaded_file(file_content, filename):
    # ... processing logic
```

### Error Tracking
```python
# Add error tracking
import traceback

def safe_process_file(file_content, filename):
    try:
        return process_uploaded_file(file_content, filename)
    except Exception as e:
        print(f"Error processing {filename}: {str(e)}")
        traceback.print_exc()
        return []
```

## 🧪 Testing Strategies

### Unit Tests
```python
# test_app.py
import unittest
from app import process_uploaded_file, get_database_info

class TestApp(unittest.TestCase):
    def test_file_processing(self):
        # Test file processing
        content = b"Test content"
        result = process_uploaded_file(content, "test.txt")
        self.assertIsInstance(result, list)
    
    def test_database_info(self):
        # Test database info
        info = get_database_info()
        self.assertIn('count', info)
```

### Integration Tests
```python
# test_integration.py
def test_full_workflow():
    # 1. Upload file
    # 2. Process file
    # 3. Query database
    # 4. Verify response
    pass
```

## 📚 Resources

### Documentation
- [Streamlit Docs](https://docs.streamlit.io/)
- [LangChain Docs](https://python.langchain.com/)
- [Chroma Docs](https://docs.trychroma.com/)
- [OpenAI API Docs](https://platform.openai.com/docs)

### Community
- [GitHub Issues](https://github.com/udit-guleria/rag-chat-assistant/issues)
- [Discussions](https://github.com/udit-guleria/rag-chat-assistant/discussions)
- [Streamlit Community](https://discuss.streamlit.io/)

### Tools
- **IDE**: VS Code, PyCharm
- **Testing**: pytest, unittest
- **Debugging**: pdb, logging
- **Profiling**: cProfile, memory_profiler

---

**Happy Coding!** 🚀

For questions or contributions, please open an issue or submit a pull request.
