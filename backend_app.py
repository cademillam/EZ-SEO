
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from your frontend

# Step 1: Scrape text from a given URL
def extract_text_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = ' '.join([p.get_text() for p in soup.find_all(['p', 'h1', 'h2', 'h3'])])
        return text[:3000]  # Limit for demo
    except Exception as e:
        return f"Error: {e}"

import os
import requests
from dotenv import load_dotenv

load_dotenv()  # This loads your .env file

def generate_keywords_with_ai(content, industry):
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
    headers = {"Authorization": f"Bearer {os.getenv('HF_API_KEY')}"}

    prompt = f"Generate 10 long-tail SEO keywords for this website content in the {industry} industry:\n\n{content[:1000]}"

    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})

    if response.status_code != 200:
        return [{"keyword": "API error", "volume": 0, "competition": "N/A"}]

    try:
        output = response.json()[0]["generated_text"]
    except Exception:
        return [{"keyword": "Parsing error", "volume": 0, "competition": "N/A"}]

    keywords = []

    for line in output.split("\n"):
        line = line.strip()
        if not line:
            continue
        if any([
            line.lower().startswith("generate"),
            "Volume:" in line,
            "Products" in line,
            "Corgea" in line,
            "Start" in line,
            "Demo" in line,
            len(line.split()) < 3
        ]):
            continue
        if line[0].isdigit() or line.startswith("-"):
            keywords.append({
                "keyword": line,
                "volume": "?",
                "competition": "?"
            })

    if not keywords:
        keywords = [{"keyword": line.strip(), "volume": "?", "competition": "?"}
                    for line in output.split("\n") if line.strip()]

    return keywords
    


@app.route('/generate_keywords', methods=['POST'])
def generate_keywords():
    data = request.get_json()
    url = data.get('url')
    industry = data.get('industry', 'general')
    mode = data.get('mode', 'seo')  # NEW: check if user wants geo or seo

    content = extract_text_from_url(url)
    if content.startswith("Error"):
        return jsonify({"error": content}), 400

    keywords = generate_keywords_with_ai(content, industry, mode=mode)  # pass mode here
    return jsonify(keywords)


if __name__ == '__main__':
    app.run(debug=True)
