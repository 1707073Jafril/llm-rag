# LLM-RAG

`llm-rag` is a Python package for Retrieval-Augmented Generation (RAG), integrating large language models with ChromaDB to augment queries with context from diverse data sources. It supports text, PDF, DOCX, XML, JSON, CSV, PPTX, and XLSX formats, enabling users to process and query external data efficiently.

## Installation

Install the package via pip:

```bash
pip install llm-rag
```

## Usage

The `process_rag` function processes input data, stores it in ChromaDB, and generates a response using the specified language model.

```python
from llm_rag import process_rag

response = process_rag(
    provider="openai",
    model="gpt-4",
    api_key="your-api-key",
    data_source=[
        "Python is great for AI.",
        {"file_path": "document.pdf"},
        {"file_path": "data.csv"},
        {"file_path": "slides.pptx"},
        {"file_path": "data.xlsx"},
        {"file_path": "config.json"},
        {"file_path": "schema.xml"}
    ],
    system_prompts="You are an expert in AI. Provide concise answers.",
    query="Why is Python used for AI?",
    persist_path="./chroma_db"
)
print(response)
```

### Parameters

- `provider`: Language model provider
- `model`: Model name 
- `api_key`: API key for the chosen provider.
- `data_source`: Text, list of texts, or list of dicts with `file_path` (e.g., `[{"file_path": "doc.pdf"}]`).
- `system_prompts`: String or list of strings for model context.
- `query`: The user’s question or prompt.
- `persist_path`: Directory for ChromaDB storage (default: `./chroma_db`).
- **Supported Formats**: text, PDF, DOCX, XML, JSON, CSV, PPTX, XLSX.

## Requirements

- Python 3.8+
- Dependencies:
  - `openai>=1.0.0`
  - `sentence-transformers>=2.2.0`
  - `chromadb>=0.4.0`
  - `anthropic>=0.3.0`
  - `PyPDF2>=3.0.0`
  - `python-docx>=0.8.0`
  - `pandas>=1.5.0`
  - `python-pptx>=0.6.0`
  - `openpyxl>=3.0.0`

## Local Testing

1. Clone the repository:

   # git clone https://github.com/1707073Jafril/llm-rag.git\
   cd llm-rag
2. Create a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Build and install the package:

   ```bash
   pip install --upgrade build
   python -m build
   pip install dist/llm_rag-0.4.0-py3-none-any.whl
   ```
4. Test with a sample script (see Usage).

## Contributing

Contributions are welcome! Please submit issues or pull requests to the GitHub repository.

## License

MIT License
