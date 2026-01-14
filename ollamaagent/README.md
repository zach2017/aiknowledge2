# Ollama Agent Demo 

Building an AI agent is like building a "digital brain" with its own memory, reasoning power, and toolbox. When you use Docker, you are essentially building a specialized, portable office for that brain to live in.

---

## 1. Top Summary: What are these parts for?

| Service | What is it? | Use Case |
| --- | --- | --- |
| **Ollama** | The LLM Engine | Provides the "Intelligence." It runs the model (like Qwen2) that understands and generates text. |
| **ChromaDB** | The Vector Memory | Provides the "Long-term Memory." It stores tasks and facts so the agent doesn't forget them when it restarts. |
| **LangChain** | The Orchestrator | The "Nervous System." It connects the LLM to the database and handles the logic of "thinking" and "acting." |
| **Docker** | The Environment | The "Container." It ensures all these parts work together on any computer without needing complex manual setup. |

---

## 2. Deep Dive: How each part works

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
