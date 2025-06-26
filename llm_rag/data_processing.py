import os
from typing import List, Union
import PyPDF2
from docx import Document
import pandas as pd

class DataProcessor:
    def __init__(self, chunk_size: int = 500):
        self.chunk_size = chunk_size

    def process_data(self, data: Union[str, List[str], List[dict]]) -> List[str]:
        """Process input data (text, files, or file paths) into text chunks."""
        documents = []
        
        if isinstance(data, str):
            if os.path.isfile(data):
                documents.extend(self._process_file(data))
            else:
                documents.extend(self._chunk_text(data))
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, str):
                    if os.path.isfile(item):
                        documents.extend(self._process_file(item))
                    else:
                        documents.extend(self._chunk_text(item))
                elif isinstance(item, dict) and "file_path" in item:
                    documents.extend(self._process_file(item["file_path"]))
        else:
            raise ValueError("Unsupported data format. Use string, list of strings, or list of dicts with 'file_path'.")

        return documents

    def _process_file(self, file_path: str) -> List[str]:
        """Extract text from file based on extension."""
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                return self._chunk_text(f.read())
        elif ext == ".pdf":
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                text = "".join(page.extract_text() for page in reader.pages if page.extract_text())
                return self._chunk_text(text)
        elif ext == ".docx":
            doc = Document(file_path)
            text = "\n".join(para.text for para in doc.paragraphs if para.text)
            return self._chunk_text(text)
        elif ext == ".csv":
            df = pd.read_csv(file_path)
            text = "\n".join(df.astype(str).agg(" ".join, axis=1))
            return self._chunk_text(text)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    def _chunk_text(self, text: str) -> List[str]:
        """Split text into chunks of specified size."""
        if not text:
            return []
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0

        for word in words:
            current_length += len(word) + 1
            if current_length > self.chunk_size:
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]
                current_length = len(word) + 1
            else:
                current_chunk.append(word)
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        return chunks