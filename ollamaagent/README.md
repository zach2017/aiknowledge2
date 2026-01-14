# Ollama Agent Demo 

Building an AI agent is like building a "digital brain" with its own memory, reasoning power, and toolbox. When you use Docker, you are essentially building a specialized, portable office for that brain to live in.

---



## Deeper Dive: How each part works

### **Ollama (The Inference Engine)**

* **What it does:** It takes a text prompt and returns a response.
* **How it works:** It loads large files (models) into your RAM. When you send a message, it uses "Inference" (mathematical guessing) to predict the next best words.
* **Why we use it:** It allows you to run high-quality AI models locally on your own CPU/GPU without paying for a subscription or sending your data to the cloud.

### **ChromaDB (The Vector Database)**

* **What it does:** It stores text not as words, but as **Vectors** (long lists of numbers).
* **The AI Concept: Embeddings:** * To an AI, the word "Apple" and "Fruit" are mathematically "close" to each other in a 3D-like space.
* ChromaDB stores these coordinates. When the agent asks, "What was my task about fruit?", ChromaDB finds "Apple" because their numbers are similar.


* **Why we use it:** Traditional databases search for exact words. ChromaDB searches for **meanings**. This allows the agent to have "semantic memory."

### **LangChain (The Logic Framework)**

* **What it does:** It creates a "Chain" of events.
* *Step 1:* Get user input.
* *Step 2:* Ask ChromaDB for relevant memory.
* *Step 3:* Send memory + input to Ollama.
* *Step 4:* Take Ollama's answer and perform an action (like scraping a site).


* **Why we use it:** It saves you from writing hundreds of lines of "glue code" to make the AI talk to the database or the internet.

---

## 3. The "Agentic" Concepts: Goals, Tasks, and Loops

For a new user, an "Agent" is different from a "Chatbot" because of three key behaviors:

1. **Task Decomposition (Planning):**
* **User Goal:** "Scrape this website."
* **Agent Logic:** It uses the LLM to break that goal into: 1. Find URL, 2. Get HTML, 3. Extract data.


2. **The ReAct Loop (Reason + Act):**
* The agent **Reasons** ("I need to find the link first").
* The agent **Acts** (Uses a tool to search).
* The agent **Observes** (Reads the search results) and repeats until the goal is met.


3. **Memory Retrieval:** * Instead of reading the entire history every time (which makes the AI slow and expensive), the agent only "pulls" the most relevant tasks from ChromaDB using a query.

---

## 4. Step-by-Step: Putting the Code Together

If you are a new user, here is how the flow looks in your project:

1. **Define the Goal:** You write a goal in a file (`tasks.json`).
2. **The Ingester (`ingest_tasks.py`):** This script uses **LangChain** to take your text, send it to **Ollama** to turn it into a "Vector," and save it in **ChromaDB**.
3. **The Worker (`agent_worker.py`):**
* It asks ChromaDB: "What is the highest priority task?"
* It sends that task to **Qwen2** and asks: "How do I do this?"
* It performs the action (e.g., uses the `requests` library to scrape).


4. **The Loop:** It saves the result back into ChromaDB and looks for the next task.

### Why Docker is the Final Piece:

Without Docker, you would have to install Python, Ollama, and ChromaDB separately and hope their versions match. With Docker, we define a `docker-compose.yml` that says: *"Create these three rooms, connect them with a private hallway (network), and make sure the Database is ready before the Agent wakes up."*

This guide expands our Dockerized AI Agent stack into a full-scale professional architecture, integrating **DevSecOps**, **Cloud concepts**, and **Automated Code Generation**.

---

## 1. Component Deep-Dive & Official Documentation

To build a production system, you must understand the "Source of Truth" for each tool.

### **The LLM Engine: Ollama**

* **What it is:** A lightweight, extensible framework for running Llama 3, Qwen2, and other models locally.
* **How it works:** It bundles model weights, configurations, and datasets into a "Modelfile," similar to a Dockerfile.
* **Official Docs:** [Ollama GitHub Documentation](https://github.com/ollama/ollama/tree/main/docs)

### **The Vector Memory: ChromaDB**

* **What it is:** An open-source embedding database designed specifically for AI workflows.
* **How it works:** It uses HNSW (Hierarchical Navigable Small World) graphs to perform "Nearest Neighbor" searches across millions of vectors in milliseconds.
* **Official Docs:** [ChromaDB Documentation](https://www.google.com/search?q=https://docs.trychroma.com/)

### **The Orchestrator: LangChain**

* **What it is:** A framework for developing applications powered by language models.
* **How it works:** It provides "Chains" (sequences of calls) and "Agents" (logic that decides which tool to use).
* **Official Docs:** [LangChain Python Docs](https://python.langchain.com/docs/get_started/introduction)

---

## 2. AI DevSecOps: Securing the Agent

In a production environment, you cannot trust AI-generated code. **AI DevSecOps** is the practice of building automated security guardrails around your agent.

### **Code Snippet: The "Security Sandbox" Check**

Before your agent executes a "Scrape" or "Command" task, use a Python guardrail to scan for malicious patterns:

```python
import re

def security_guardrail(generated_code):
    # Prohibit dangerous system calls
    forbidden_commands = ["rm -rf", "os.system", "subprocess.Popen", "chmod"]
    for cmd in forbidden_commands:
        if cmd in generated_code:
            raise PermissionError(f"Security Alert: Agent attempted forbidden command: {cmd}")
    
    # Check for IP exfiltration patterns
    if re.search(r"\b\d{1,3}(\.\d{1,3}){3}\b", generated_code):
        print("Warning: Potential IP address detected in generated output.")
    
    return True

```

---

## 3. Training a Vector DB for "System Config"

One of the best use cases for a Vector DB is **RAG (Retrieval-Augmented Generation)** for system administration. You can "train" (index) your entire company's server configurations so the agent can fix bugs.

### **Template: Configuration Indexer**

This script takes local Nginx or Docker configs and stores them in ChromaDB so the agent knows how your "Cloud" is set up.

```python
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import CharacterTextSplitter

# 1. Load your infrastructure files
with open("nginx.conf") as f:
    config_data = f.read()

# 2. Split into chunks (AI handles small pieces better)
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.create_documents([config_data])

# 3. Store in Chroma
vectorstore = Chroma.from_documents(
    documents=docs, 
    embedding=OllamaEmbeddings(model="nomic-embed-text"),
    persist_directory="./chroma_db"
)

print("System configuration indexed for Agent retrieval.")

```

---

## 4. Evolution of AI Agents (A Short History)

* **2020 (The Prompt Era):** GPT-3 arrives. Users "chat," but the AI has no memory and cannot "do" anything.
* **2022 (The Chain Era):** LangChain is released. We begin connecting LLMs to APIs and databases.
* **2023 (The Agent Era):** **AutoGPT** and **BabyAGI** show that AI can loop: it can create its own tasks, execute them, and learn from the results.
* **2024+ (The Sovereign Era):** Local models (Ollama/Qwen) and Docker allow agents to run entirely offline, securely, and within private clouds.

---

## 5. Use Cases: From Simple to Complex

### **Level 1: The Simple Researcher (Search & Summarize)**

* **Logic:** Agent reads a `tasks.json` containing URLs.
* **Tools:** `requests` + `Ollama`.
* **Goal:** Summarize the latest news from a specific site every morning.

### **Level 2: The DevOps Junior (Log Analysis)**

* **Logic:** Agent monitors a Docker log file. When it sees an "Error 500," it queries ChromaDB for the "How-To-Fix" documentation.
* **Tools:** `Docker API` + `ChromaDB`.
* **Goal:** Automatically suggest a fix or restart a crashed container.

### **Level 3: The Complex Architect (Self-Healing Cloud)**

* **Logic:** The agent has access to your Cloud (AWS/Azure) CLI tools.
* **Tools:** `Terraform` + `Ollama` + `LangChain Agents`.
* **Goal:** You give a goal ("Make the website handle 10k users"). The agent writes the Terraform code, scans it for security (DevSecOps), applies the change to the cloud, and verifies the site is up.


