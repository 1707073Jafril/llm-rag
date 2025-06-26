from typing import Union, List
from .vector_db import ChromaVectorStore
from .models import get_model_client
from .data_processing import DataProcessor

def process_rag(
    provider: str,
    model: str,
    api_key: str,
    data_source: Union[str, List[str], List[dict]],
    system_prompts: Union[str, List[str]],
    query: str
) -> str:
    """Process RAG pipeline and return response."""
    if not api_key:
        raise ValueError("API key is required")
    
    # Initialize components
    provider = provider.lower()
    client = get_model_client(provider, api_key, model)
    vector_store = ChromaVectorStore()
    data_processor = DataProcessor()

    # Process and store data
    documents = data_processor.process_data(data_source)
    vector_store.add_documents(documents)

    # Retrieve relevant documents
    relevant_docs = vector_store.search(query, k=3)
    context = "\n".join(relevant_docs)

    # Prepare system prompt
    system_prompt = system_prompts if isinstance(system_prompts, str) else "\n".join(system_prompts)
    
    # Prepare full prompt
    prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"

    # Generate response
    if provider == "openai":
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    
    elif provider == "claude":
        response = client.messages.create(
            model=model,
            max_tokens=500,
            system=system_prompt,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text.strip()
    
    elif provider == "gemini":
        response = client.generate_content(f"{system_prompt}\n{prompt}")
        return response.text.strip()
    
    elif provider == "deepseek":
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    
    else:
        raise ValueError(f"Unsupported provider: {provider}")