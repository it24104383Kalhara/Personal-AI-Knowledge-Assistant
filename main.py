import argparse
import os       # To check file extensions
import sys      # To exit program gracefully
from src.rag_engine import (read_and_chunk_text, find_relevant_chunk, get_ai_answer)        # Import RAG engine

def setup_arg_parser():
    """Sets up and parse command-line arguments."""
    parser = argparse.ArgumentParser(description="AI Knowledge Assistant CLI")

    # Define th first argument: file path
    parser.add_argument(
        "filepath",
        type=str,
        help="The full path to the text file to use as context."
    )

    # Define the second argument: question
    parser.add_argument(
        "question",
        type=str,
        help="The question to ask the AI."
    )
    return parser.parse_args()


# --- Define the main functions ---
def run_rag_pipeline(filepath, question):
    """Executes the complete RAG Pipeline:
    Load -> Chunk -> Retrieve -> Augment & Generate
    """
    try:
        # Check file path
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Error: The file {filepath} not found.")

        # Check file extension
        if not filepath.lower().endswith('.txt'):
            raise ValueError("Error: This tool currently only support .txt files.")

        print("--- Running AI Knowledge Assistant ---")
        print(f"Filepath: {filepath}")
        print(f"User Question: {question}\n")

        # Load & chunk
        chunks = read_and_chunk_text('sample_text.txt')

        # Empty file check
        if not chunks:
            raise ValueError("Error: The file '{filepath}' is empty or contains no text.")

        print(f"Loaded {len(chunks)} chunks from {filepath}\n")

        # Retrieve
        relevant_chunk = find_relevant_chunk(chunks, question)

        if not relevant_chunk:
            print("No relevant context found.")
            print("Could not find a relevant chunk for the question. The AI will answer based on its general knowledge.")
            relevant_chunk = None
        else:
            print("--- Found relevant context ---")
            print(f"{relevant_chunk}\n")

            # Augment and generate
            print("--- Sending to AI for answer ---")
            final_answer = get_ai_answer(relevant_chunk, question)

            print("\n--- FINAL ANSWER ---")
            print(final_answer)
    except FileNotFoundError as e:
        print(str(e))       # prints firendly error we created 
        sys.exit(1)         # Exit with a non-zero status code (indicates error) 
    except ValueError as e:
        print(str(e))       # prints firendly validation errors
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
    

# --- Run the Script ---
# This special block ensures the code only runs
if __name__ == "__main__":
    args = setup_arg_parser()   
    run_rag_pipeline(args.filepath, args.question)
