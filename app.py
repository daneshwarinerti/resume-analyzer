from flask import Flask, render_template, request
import os
from analyzer import extract_text_from_pdf, analyze_resume  # Import functions from analyzer.py

# Initialize Flask app
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create uploads folder if it doesn't exist

# Home route (upload page)
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle resume upload and analysis
@app.route('/analyze', methods=['POST'])
def analyze():
    # Check if file is uploaded
    if 'resume' not in request.files:
        return "No file uploaded", 400

    file = request.files['resume']
    if file.filename == '':
        return "No selected file", 400

    # Save the uploaded PDF
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Extract text from PDF
    text = extract_text_from_pdf(filepath)

    # Analyze resume (skills, score, suggestions)
    result = analyze_resume(text)

    # Render results page with data
    return render_template(
        'result.html',
        skills=result["skills"],
        missing=result["missing_skills"],
        score=result["score"],
        suggestions=result["suggestions"]
    )

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

