import os
import requests
from dotenv import load_dotenv 

# --- 1. Load the API ---
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Make sure it's set in your .env file.")

# --- 2. File Reading and Chunking ---
def read_and_chunk_text(filepath):
    """Reads a text file and splits it into chunks based on empty lines."""
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Split the text by double newlines (paragraphs)
    chunks = content.split('\n\n')
    
    # Clean up any extra whitespace from the chunks
    cleaned_chunks = [chunk.strip() for chunk in chunks if chunk.strip()]
    return cleaned_chunks

# --- 3. Basic Keyword Search ---
def find_relevant_chunk(chunks, question):
    """Find most relevant chunks based on keyword matching"""
    # List of 'stop-words' to ignore
    stop_words = {'what', 'is', 'the', 'a', 'of','in'}


    # Strip punctuation from the words to make it more accurate
    question_keywords = {
        word.strip('.,?!')
        for word in question.lower().split()
        if word.strip('.,?!') not in stop_words
    }

    best_chunk = None
    max_score = 0

    for chunk in chunks:
        # Also strip punctuation from chunk words
        chunk_words = {word.strip('.,?!') for word in chunk.lower().split()}
        score = len(question_keywords.intersection(chunk_words))

        if score > max_score:
            max_score = score
            best_chunk = chunk
    return best_chunk

# --- 4. Call API key to generate the answer ---
def get_ai_answer(context, question):
    # This is the Augmented prompt
    augmented_prompt = f"""
    Context:
    {context}

    Question:
    {question}
    Based *only* on the context provided, answer the question.
    """

    api_url = "https://api.openai.com/v1/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Context-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo-instruct",
        "prompt":augmented_prompt,
        "max_tokens": 100
    }

    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()     # Raise en error for bad responses
        response_data = response.json()

        if "choices" in response_data and len(response_data["choices"]) > 0:
            return response_data["choices"][0]["text"].strip()
        else:
            return "Error: No valid response from AI."
    except requests.exceptions.HTTPError as http_error:
        return f"HTTP error occurred: {http_error}"
    except Exception as e:
        return f"Other error occurred: {e}"
