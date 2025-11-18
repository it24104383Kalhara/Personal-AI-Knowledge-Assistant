import os
import requests
from dotenv import load_dotenv

# --- 1. Load Environment Variables ---
# This line loads the OPENAI_API_KEY from your .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OpenAI API key not found. Make sure it's set in your .env file.")

# --- 2. Prepare API Request ---
# We are using the "gpt-3.5-turbo-instruct" model, a great model for simple prompts
api_url = "https://api.openai.com/v1/completions"

# This tells the API who you are (your key)
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# This is the data we're sending. We're asking the AI to say "Hello World!"
data = {
    "model": "gpt-3.5-turbo-instruct", # This is a fast, low-cost model
    "prompt": "Say 'Hello, World!'",
    "max_tokens": 10
}

# --- 3. Send the Request ---
try:
    response = requests.post(api_url, headers=headers, json=data)
    
    # This checks if the request was successful (e.g., code 200)
    response.raise_for_status() 

    response_data = response.json()
    
    # --- 4. Print the AI's Answer ---
    if "choices" in response_data and len(response_data["choices"]) > 0:
        ai_response = response_data["choices"][0]["text"]
        print("--- API Call Successful! ---")
        print(f"AI Response: {ai_response.strip()}") # .strip() removes extra whitespace
    else:
        print("Error: No valid response received from AI.")
        print(response_data)

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
    print(f"Response content: {response.text}")
except Exception as err:
    print(f"Other error occurred: {err}")