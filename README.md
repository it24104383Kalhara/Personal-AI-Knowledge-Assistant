# Personal AI Knowledge Assistant

This project is a command-line AI assistant that uses Retrieval-Augmented Generation (RAG) to answer questions based on a text document you provide.

---

## 🚀 How to Run

This project requires Python 3.8+ and an OpenAI API key.

### 1. Setup

**Clone the repository:**
```bash
git clone [https://github.com/it24104383Kalhara/Personal-AI-Knowledge-Assistant.git](https://github.com/it24104383Kalhara/Personal-AI-Knowledge-Assistant.git)
cd Personal-AI-Knowledge-Assistant
```
**Create a virtual environment:**
```bash
python -m venv my_assistant_env
.\my_assistant_env\Scripts\activate
```
**Install required libraries:**
```bash
pip install -r requirements.txt
```
**Create your environment file:**
```
1. Create a file named .env in the root folder.

2. Add your OpenAI API key to it: OPENAI_API_KEY="sk-..."
```
### 2. Run the Tool
``` 
python main.py "path/to/your/document.txt" "Your question about the document?"
```
**Example:**
```
python main.py "sample_text.txt" "What is the currency of Japan?"
```
**Example Output:**
```
--- Running AI Knowledge Assistant ---
Filepath: sample_text.txt
User Question: What is the currency of Japan?

Loaded 2 chunks from sample_text.txt

--- Found Relevant Context ---
The capital of Japan is Tokyo...
...The currency of Japan is the Yen.

--- Sending to AI for Answer ---

--- FINAL ANSWER ---
The currency of Japan is the Yen.
```
