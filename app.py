import streamlit as st
import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import openai

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.environ.get('OPENAI_API_KEY')

# Configuration
CHROMA_PATH = "chroma"
PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'db' not in st.session_state:
    st.session_state.db = None

def initialize_database():
    """Initialize the Chroma database"""
    try:
        embedding_function = OpenAIEmbeddings()
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
        return db
    except Exception as e:
        st.error(f"Error initializing database: {str(e)}")
        return None

def query_database(question, db):
    """Query the database and return results"""
    try:
        # Search the database
        results = db.similarity_search_with_relevance_scores(question, k=3)
        
        if len(results) == 0 or results[0][1] < 0.7:
            return None, "Unable to find matching results. Please try rephrasing your question."
        
        # Prepare context
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        
        # Create prompt
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=question)
        
        # Get response from OpenAI
        model = ChatOpenAI()
        response_text = model.predict(prompt)
        
        # Get sources
        sources = [doc.metadata.get("source", "Unknown") for doc, _score in results]
        
        return response_text, sources
    except Exception as e:
        return None, f"Error processing query: {str(e)}"

def main():
    st.set_page_config(
        page_title="RAG Chat Assistant",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Header
    st.title("🤖 RAG Chat Assistant")
    st.markdown("Ask questions about Alice in Wonderland and get AI-powered answers!")
    
    # Sidebar
    with st.sidebar:
        st.header("📚 About")
        st.markdown("""
        This is a Retrieval-Augmented Generation (RAG) application that allows you to ask questions about Alice in Wonderland.
        
        The system:
        1. Searches through the book content
        2. Finds relevant passages
        3. Uses AI to generate answers based on the content
        """)
        
        st.header("⚙️ Settings")
        if st.button("🔄 Refresh Database"):
            st.session_state.db = None
            st.rerun()
    
    # Check if database is initialized
    if st.session_state.db is None:
        with st.spinner("Initializing database..."):
            st.session_state.db = initialize_database()
    
    if st.session_state.db is None:
        st.error("❌ Failed to initialize database. Please check your setup and try again.")
        st.stop()
    
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
        - Ask specific questions
        - Try character names
        - Ask about plot events
        - Be descriptive in your queries
        """)
        
        # Example questions
        st.markdown("### 🔍 Example Questions")
        example_questions = [
            "How does Alice meet the Mad Hatter?",
            "What happens at the tea party?",
            "Who is the Cheshire Cat?",
            "What is the Queen of Hearts like?",
            "How does Alice get to Wonderland?"
        ]
        
        for question in example_questions:
            if st.button(question, key=f"example_{question}"):
                st.session_state.user_input = question
                st.rerun()
    
    # Chat input
    if prompt := st.chat_input("Ask a question about Alice in Wonderland..."):
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

