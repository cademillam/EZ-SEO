
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

# Step 2: Placeholder for AI keyword generation
def generate_keywords_with_ai(content, industry):
    # In production: replace this with a call to LLaMA/OpenAI
    return [
        {"keyword": "best seo tools for small businesses", "volume": 1000, "competition": "Low"},
        {"keyword": "how to rank on google in 2024", "volume": 880, "competition": "Medium"},
        {"keyword": "seo keyword research for beginners", "volume": 720, "competition": "Medium"},
        {"keyword": "long tail keywords example", "volume": 600, "competition": "Low"},
        {"keyword": "free seo audit tools", "volume": 500, "competition": "High"}
    ]

@app.route('/generate_keywords', methods=['POST'])
def generate_keywords():
    data = request.get_json()
    url = data.get('url')
    industry = data.get('industry', 'general')

    # Extract content from URL
    content = extract_text_from_url(url)
    if content.startswith("Error"):
        return jsonify({"error": content}), 400

    # Use AI (placeholder) to generate keywords
    keywords = generate_keywords_with_ai(content, industry)
    return jsonify(keywords)

if __name__ == '__main__':
    app.run(debug=True)
