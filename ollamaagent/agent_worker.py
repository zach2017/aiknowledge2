import os
import time
import chromadb
import requests
from langchain_community.llms import Ollama

# Configuration
CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Initialize
client = chromadb.HttpClient(host=CHROMA_HOST, port=8000)
collection = client.get_or_create_collection(name="agent_tasks")
llm = Ollama(model="qwen2:7b", base_url=OLLAMA_URL)

def perform_scrape(url):
    print(f"--- Executing Scrape on: {url} ---")
    try:
        # Simple scraping logic
        response = requests.get(url, timeout=10)
        text_snippet = response.text[:500] # Get first 500 chars
        return text_snippet
    except Exception as e:
        return f"Error: {str(e)}"

def run_agent_loop():
    print("Agent started. Looking for tasks...")
    
    # 1. Get the most relevant task from Chroma
    results = collection.peek(limit=1)
    
    if results['ids']:
        task_id = results['ids'][0]
        metadata = results['metadatas'][0]
        print(f"Found Task: {metadata['goal']}")

        # 2. Perform Action
        if metadata['action'] == "Scrape":
            data = perform_scrape(metadata['params'])
            
            # 3. Use Ollama to summarize the scraped data
            summary = llm.invoke(f"Summarize this raw HTML/Text content for the goal '{metadata['goal']}': {data}")
            print(f"Agent Result: {summary}")
            
            # 4. Clean up (Remove task from queue once done)
            collection.delete(ids=[task_id])
    else:
        print("No tasks found in queue.")

if __name__ == "__main__":
    # Wait for Chroma/Ollama to be fully ready
    time.sleep(10) 
    run_agent_loop()