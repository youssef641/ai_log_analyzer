from langchain_community.llms import Ollama
from config import OLLAMA_MODEL

def summarize_logs_with_ollama(logs):
    llm = Ollama(model=OLLAMA_MODEL)
    prompt = "Summarize the following logs:\n" + "\n".join(logs[:100])
    response = llm.invoke(prompt)
    return response
