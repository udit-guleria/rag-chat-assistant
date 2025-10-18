#!/usr/bin/env python3
"""
Document management utility for the Multi-Document RAG application.
This script helps manage documents in the database.
"""

import os
import shutil
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# Load environment variables
load_dotenv()

CHROMA_PATH = "chroma"

def get_database_info():
    """Get information about documents in the database"""
    try:
        if not os.path.exists(CHROMA_PATH):
            return {"count": 0, "sources": [], "chunks": []}
        
        embedding_function = OpenAIEmbeddings()
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
        
        # Get all documents
        all_docs = db.get()
        sources = set()
        chunks_info = []
        
        for i, metadata in enumerate(all_docs.get('metadatas', [])):
            if 'source' in metadata:
                sources.add(metadata['source'])
                chunks_info.append({
                    'id': all_docs.get('ids', [])[i],
                    'source': metadata.get('source', 'Unknown'),
                    'upload_id': metadata.get('upload_id', 'N/A'),
                    'start_index': metadata.get('start_index', 0)
                })
        
        return {
            "count": len(all_docs.get('ids', [])), 
            "sources": list(sources),
            "chunks": chunks_info
        }
    except Exception as e:
        print(f"Error getting database info: {str(e)}")
        return {"count": 0, "sources": [], "chunks": []}

def clear_database():
    """Clear the entire database"""
    try:
        if os.path.exists(CHROMA_PATH):
            shutil.rmtree(CHROMA_PATH)
            print("✅ Database cleared successfully!")
        else:
            print("ℹ️  No database found to clear.")
    except Exception as e:
        print(f"❌ Error clearing database: {str(e)}")

def list_documents():
    """List all documents in the database"""
    info = get_database_info()
    
    print(f"📊 Database Status:")
    print(f"   Total chunks: {info['count']}")
    print(f"   Unique documents: {len(info['sources'])}")
    
    if info['sources']:
        print(f"\n📁 Documents in database:")
        for i, source in enumerate(info['sources'], 1):
            print(f"   {i}. {source}")
    else:
        print("\n📭 No documents found in database.")

def search_documents(query):
    """Search for documents containing specific text"""
    try:
        if not os.path.exists(CHROMA_PATH):
            print("❌ No database found.")
            return
        
        embedding_function = OpenAIEmbeddings()
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
        
        results = db.similarity_search(query, k=5)
        
        print(f"🔍 Search results for '{query}':")
        for i, doc in enumerate(results, 1):
            source = doc.metadata.get('source', 'Unknown')
            content_preview = doc.page_content[:100] + "..." if len(doc.page_content) > 100 else doc.page_content
            print(f"\n{i}. Source: {source}")
            print(f"   Preview: {content_preview}")
            
    except Exception as e:
        print(f"❌ Error searching documents: {str(e)}")

def main():
    print("📚 Multi-Document RAG - Document Manager")
    print("=" * 40)
    
    while True:
        print("\nOptions:")
        print("1. List documents")
        print("2. Search documents")
        print("3. Clear database")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            list_documents()
        elif choice == "2":
            query = input("Enter search query: ").strip()
            if query:
                search_documents(query)
        elif choice == "3":
            confirm = input("⚠️  Are you sure you want to clear the database? (y/N): ").strip().lower()
            if confirm == 'y':
                clear_database()
            else:
                print("❌ Operation cancelled.")
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-4.")

if __name__ == "__main__":
    main()
