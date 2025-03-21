import os
import docx2txt
from collections import Counter
from flask import Flask, request, render_template, redirect

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Local stopword list (without nltk)
stop_words = {
    'is', 'that', 'a', 'the', 'and', 'to', 'in', 'of', 'for', 'on', 'by',
    'with', 'an', 'this', 'it', 'as', 'from', 'or', 'at', 'which', 'be',
    'are', 'was', 'were', 'but', 'not', 'so', 'if', 'also', 'such', 'can', 
    'have', 'has', 'had', 'into', 'about', 'explain', 'describe', 'discuss', 
    'elaborate', 'write', 'note', 'summarize'
}

# Keywords coming from your keywords.js
custom_keywords = [
    'desalination', 'reverse osmosis', 'electro spinning', 'nano-material', 
    'metal matrix', 'polymer matrix', 'bergious process', 'orsat method', 
    'solar cell', 'lithium ion battery', 'demineralization', 'sol-gel', 
    'ceramic matrix', 'otto hoffman', 'wind energy', 'geothermal energy', 
    'nanocluster', 'nanowires', 'nuclear power plant', 'berger process'
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'files[]' not in request.files:
        return redirect(request.url)
    
    files = request.files.getlist('files[]')
    combined_text = ""

    for file in files:
        if file.filename.endswith('.docx'):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            text = docx2txt.process(filepath)
            combined_text += text + "\n"

    # Preprocess text
    words = combined_text.lower().split()
    filtered_words = [word for word in words if word.isalpha() and word not in stop_words]
    word_freq = Counter(filtered_words)

    matched_questions = []

    # Split by line assuming each question is on a separate line
    for question in combined_text.split('\n'):
        matched = False
        for keyword in custom_keywords:
            if keyword in question.lower():
                matched_questions.append(question)
                matched = True
                break
        if not matched:
            for word, count in word_freq.items():
                if count >= 2 and word in question.lower():
                    matched_questions.append(question)
                    break

    if matched_questions:
        return render_template('result.html', questions=matched_questions)
    else:
        return render_template('result.html', questions=['No important questions found based on keywords.'])

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
