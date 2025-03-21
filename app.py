from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)
load_dotenv()  # Load variables from .env

# API Keys (Replace with actual keys)
HF_API_KEY = os.getenv("HF_API_KEY")
JOOBLE_API_KEY = os.getenv("JOOBLE_API_KEY")
GOOGLE_CSE_API_KEY = os.getenv("GOOGLE_CSE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

# API URLs
HF_API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"
JOOBLE_API_URL = f"https://jooble.org/api/{JOOBLE_API_KEY}"
GOOGLE_CSE_URL = f"https://www.googleapis.com/customsearch/v1"

HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

@app.route('/recommend', methods=['POST'])
def recommend_career():
    data = request.json
    education = data.get("education", "")
    skills = data.get("skills", "")
    interests = data.get("interests", "")

    prompt = f"Suggest a suitable career for someone with a {education} degree, skills in {skills}, and interest in {interests}."

    response = requests.post(HF_API_URL, headers=HEADERS, json={"inputs": prompt})

    if response.status_code == 200:
        result = response.json()
        if isinstance(result, list) and len(result) > 0 and 'generated_text' in result[0]:
            recommended_career = result[0]['generated_text']
            return jsonify({"recommended_career": recommended_career})
    
    return jsonify({"error": "Career recommendation failed"}), 500

@app.route('/jobs', methods=['POST'])
def get_jobs():
    data = request.json
    career = data.get("career", "")

    job_data = {
        "keywords": career,
        "location": "India",
        "page": 1,
        "searchMode": "1"
    }

    response = requests.post(JOOBLE_API_URL, headers={"Content-Type": "application/json"}, json=job_data)

    if response.status_code == 200:
        jobs = response.json()
        return jsonify(jobs)
    
    return jsonify({"error": "Job search failed"}), 500

@app.route('/courses', methods=['POST'])
def get_courses():
    data = request.json
    career = data.get("career", "")

    params = {
        "key": GOOGLE_CSE_API_KEY,
        "cx": GOOGLE_CSE_ID,
        "q": f"Online courses for {career}"
    }

    response = requests.get(GOOGLE_CSE_URL, params=params)

    if response.status_code == 200:
        courses = response.json()
        return jsonify(courses)

    return jsonify({"error": "Course search failed"}), 500

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if PORT is not set
    app.run(host="0.0.0.0", port=port, debug=True)
