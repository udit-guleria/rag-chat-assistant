# 📄 Supported File Formats

This document outlines all the file formats supported by the Universal Document RAG Assistant.

## ✅ Fully Supported Formats

### 📝 Text Files
| Format | Extension | Description | Use Cases |
|--------|-----------|-------------|-----------|
| **Plain Text** | `.txt` | Simple text files | Notes, logs, documentation |
| **Markdown** | `.md` | Markdown formatted text | Documentation, README files, articles |
| **HTML** | `.html`, `.htm` | Web pages | Web content, reports |

### 📄 Documents
| Format | Extension | Description | Use Cases |
|--------|-----------|-------------|-----------|
| **PDF** | `.pdf` | Portable Document Format | Research papers, reports, manuals |
| **Word** | `.docx`, `.doc` | Microsoft Word documents | Reports, letters, documents |
| **PowerPoint** | `.ppt`, `.pptx` | Presentation files | Slides, presentations, training materials |

### 📊 Data Files
| Format | Extension | Description | Use Cases |
|--------|-----------|-------------|-----------|
| **CSV** | `.csv` | Comma-separated values | Data analysis, spreadsheets |
| **Excel** | `.xlsx`, `.xls` | Microsoft Excel files | Financial data, reports, analysis |
| **JSON** | `.json` | JavaScript Object Notation | APIs, configuration, structured data |

## 🔧 Technical Details

### Document Processing Pipeline
1. **File Upload**: Files are uploaded through the web interface
2. **Type Detection**: Automatic detection based on file extension
3. **Content Extraction**: Specialized loaders extract text content
4. **Text Chunking**: Content is split into manageable chunks (300 chars with 100 overlap)
5. **Embedding**: Chunks are converted to vector embeddings
6. **Storage**: Embeddings stored in Chroma vector database
7. **Query**: Semantic search across all document chunks

### Supported Loaders
- **TextLoader**: Plain text files
- **UnstructuredMarkdownLoader**: Markdown files
- **UnstructuredHTMLLoader**: HTML files
- **PyPDFLoader**: PDF documents
- **Docx2txtLoader**: Word documents
- **UnstructuredWordDocumentLoader**: Advanced Word processing
- **UnstructuredPowerPointLoader**: PowerPoint files
- **CSVLoader**: CSV data files
- **JSONLoader**: JSON data
- **UnstructuredExcelLoader**: Excel spreadsheets

## 🚀 Usage Examples

### Upload Multiple File Types
```python
# The web interface supports batch upload of mixed file types
# Example: Upload a research paper (PDF), presentation (PPTX), and data (CSV) together
```

### Query Across All Formats
```python
# Ask questions that span multiple document types
# Example: "What are the key findings from the research paper and presentation?"
```

## ⚠️ Limitations

### File Size
- **Recommended**: Files under 50MB for optimal performance
- **Maximum**: 200MB per file (Streamlit limitation)
- **Large Files**: Consider splitting into smaller chunks

### Content Quality
- **Text Quality**: Better results with well-formatted documents
- **OCR**: No automatic OCR for scanned PDFs (text-based PDFs only)
- **Images**: Image content is not processed (text extraction only)

### Format-Specific Notes
- **PDF**: Works best with text-based PDFs, not scanned images
- **Excel**: Processes text content, not formulas or charts
- **PowerPoint**: Extracts text from slides, not images or videos
- **HTML**: Extracts text content, not styling or scripts

## 🔄 Fallback Handling

### Unsupported Formats
If a file type is not directly supported:
1. **Text Fallback**: Attempts to read as plain text
2. **Encoding Detection**: Tries UTF-8 decoding
3. **Error Handling**: Clear error messages for unsupported formats

### Conversion Recommendations
For unsupported formats, consider converting to:
- **Images → Text**: Use OCR tools first
- **Audio/Video → Text**: Use transcription services
- **Binary → Text**: Convert to supported formats

## 📈 Performance Tips

### Optimal File Preparation
1. **Clean Text**: Remove unnecessary formatting
2. **Consistent Structure**: Use headings and sections
3. **Reasonable Size**: Split large documents into logical sections
4. **Quality Content**: Well-written documents produce better results

### Batch Processing
- **Multiple Files**: Upload related documents together
- **Mixed Formats**: Combine different file types for comprehensive knowledge base
- **Incremental Updates**: Add new documents to existing database

## 🛠️ Troubleshooting

### Common Issues
1. **File Upload Fails**: Check file size and format
2. **Poor Results**: Ensure documents contain relevant text content
3. **Encoding Errors**: Try converting to UTF-8 text format
4. **Memory Issues**: Process large files in smaller batches

### Getting Help
- Check the error messages in the web interface
- Use the document manager CLI for debugging
- Verify file format and content quality
- Try converting to a supported format

## 🎯 Best Practices

### Document Organization
- **Logical Grouping**: Upload related documents together
- **Clear Naming**: Use descriptive filenames
- **Version Control**: Keep track of document versions
- **Regular Updates**: Refresh your knowledge base regularly

### Query Optimization
- **Specific Questions**: Ask detailed, specific questions
- **Context Awareness**: Reference document types in questions
- **Iterative Refinement**: Refine questions based on results
- **Source Verification**: Always check source documents for accuracy
