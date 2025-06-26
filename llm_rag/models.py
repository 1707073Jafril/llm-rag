from openai import OpenAI
from anthropic import Anthropic


def get_model_client(provider : str, api_key : str, model : str, base_url : str = None):
    if(provider == "openai"):
        client = OpenAI(api_key = api_key)
        return client
    
    elif(provider == "anthropic"):
        client = Anthropic(api_key = api_key)
        return client
    
    else:
        return ValueError(f"Unsupported Provider : {provider}")
