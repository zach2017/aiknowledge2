import json
import chromadb
import os

# Connect to the ChromaDB container
client = chromadb.HttpClient(host="localhost", port=8000)
collection = client.get_or_create_collection(name="agent_tasks")

def load_tasks_to_chroma(file_path):
    with open(file_path, 'r') as f:
        tasks = json.load(f)

    for task in tasks:
        collection.add(
            ids=[task["id"]],
            documents=[task["description"]], # The "content" for vector search
            metadatas=[{
                "goal": task["goal"],
                "action": task["action"],
                "params": task["parameters"]
            }]
        )
    print(f"Successfully loaded {len(tasks)} tasks into ChromaDB.")

if __name__ == "__main__":
    load_tasks_to_chroma("tasks.json")