import os
from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.utils import secure_filename
from src.rag_engine import (read_and_chunk_text, find_relevant_chunk, get_ai_answer)

#  application object
app = Flask(__name__)

# secret key for sessions
app.secret_key = 'super_secret_key_for_dev_only'        # required to use the 'session' object securely

# Configuration: Tell Flask where to save uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def home():
    answer=None

    if request.method == 'POST':
        user_question = request.form.get('question')
        uploaded_file = request.files.get('document')
        
        if uploaded_file and uploaded_file.filename != '':
            # Secure the filename (prevents hacking attempts) 
            filename = secure_filename(uploaded_file.filename)

            # save the file
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            uploaded_file.save(file_path)

            try: 
                chunks = read_and_chunk_text(file_path)
                relevant_chunk = find_relevant_chunk(chunks, user_question)
                if relevant_chunk:         
                    answer = get_ai_answer(relevant_chunk, user_question)
                else:
                    answer = "I couldn't find relevant information in the document."   
            except Exception as e:
                answer = f"Error processing file: {str(e)}"
        else:
            answer = "No file uploaded. Please select a .txt file."

        # store answer in a session and redirect
        session['answer'] = answer
        return redirect(url_for('home'))
    
    # Delete the answer from the session
    answer = session.pop('answer', None)
    return render_template('index.html', answer=answer)            


# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=8888)           # debug=True allows the server to auto-reload when you change code


