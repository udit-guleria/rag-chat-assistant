# Universal Document RAG Assistant

A powerful Retrieval-Augmented Generation (RAG) application that allows you to upload documents in various formats (PDF, Word, PowerPoint, Excel, CSV, JSON, HTML, Markdown, Text) and ask questions about them using AI.

## ✨ Features

- **📁 File Upload**: Upload documents in multiple formats (PDF, Word, PowerPoint, Excel, CSV, JSON, HTML, Markdown, Text)
- **🤖 AI Chat**: Ask questions about your documents and get intelligent answers
- **📖 Source Attribution**: See exactly which documents and sections were used for each answer
- **💬 Chat History**: Maintain conversation context during your session
- **📊 Document Management**: View, search, and manage your document collection
- **🎨 Modern UI**: Clean, responsive interface built with Streamlit

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up OpenAI API Key

Create a `.env` file in the project directory:

```bash
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

### 3. Launch the Application

```bash
python run_ui.py
```

The web interface will open at `http://localhost:8501`

## 📚 How to Use

1. **Upload Documents**: Use the sidebar to upload files in various formats
2. **Ask Questions**: Chat with your documents using natural language
3. **View Sources**: Expand the "Sources" section to see which documents were used
4. **Manage Documents**: View document statistics and clear the database if needed

### Example with Alice in Wonderland

1. **Create Database**: Run `python create_database_simple.py` to process Alice in Wonderland
2. **Launch UI**: Run `python run_ui.py` to start the web interface
3. **Ask Questions**: Chat about Alice in Wonderland content

## 🛠️ Additional Tools

### Document Manager
```bash
python document_manager.py
```
- List all documents in the database
- Search for specific content
- Clear the database
- View document statistics

### Command Line Interface
```bash
python query_data.py "Your question here"
```

## 📁 Project Structure

```
├── app.py                    # Universal Streamlit app (all formats)
├── run_ui.py                 # Launcher script
├── start_ui.bat              # Windows batch file
├── document_manager.py       # Document management utility
├── create_database_simple.py # Database creation script (Alice in Wonderland)
├── query_data.py             # Command line interface
├── requirements.txt          # Dependencies
├── SUPPORTED_FORMATS.md      # Format documentation
└── README.md                # This file
```

## 🔧 Requirements

- Python 3.8+
- OpenAI API key
- Internet connection for AI responses

## 📖 Example Questions

- "What is this document about?"
- "Summarize the main points"
- "What are the key concepts?"
- "Find information about [specific topic]"
- "What are the important details?"

## 🎯 Use Cases

- **Research**: Upload research papers and ask questions
- **Documentation**: Query technical documentation
- **Learning**: Upload textbooks and study materials
- **Content Analysis**: Analyze articles, reports, or any text content
- **Knowledge Management**: Build a searchable knowledge base

## 🚀 Advanced Features

- **Multi-Document Support**: Upload and query multiple documents simultaneously
- **Source Attribution**: Always know which document provided the answer
- **Document Statistics**: Track how many documents and chunks are in your database
- **Flexible Upload**: Support for both individual files and batch uploads
- **Database Management**: Easy database clearing and management tools

> **Note**: You'll need to set up an OpenAI account and API key for the AI responses to work.

## 📚 Documentation

### Quick Start
- **README.md** - This file (quick start guide)
- **PROJECT_DOCUMENTATION.md** - Complete project documentation
- **DEVELOPER_GUIDE.md** - Developer information and customization
- **SUPPORTED_FORMATS.md** - Detailed file format documentation

### Setup Scripts
- **setup.py** - Automated setup script for new users
- **start_ui.bat** - Windows batch launcher
- **run_ui.py** - Python launcher script

### Tools
- **document_manager.py** - CLI document management
- **query_data.py** - Command-line query interface
- **create_database_simple.py** - Sample database creation

## 📺 Tutorial Video

Original tutorial: [RAG+Langchain Python Project: Easy AI/Chat For Your Docs](https://www.youtube.com/watch?v=tcqEUSNCn8I&ab_channel=pixegami)