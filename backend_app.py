
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import random

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

def generate_keywords_with_ai(content, mode="seo"):
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
    headers = {"Authorization": f"Bearer {os.getenv('HF_API_KEY')}"}

    if mode == "geo":
        prompt = (
            f"Generate 10 concise questions that a user would ask a search assistant about the following website content. "
            f"Focus on the core information and services the website provides. "
            f"Identify key terms and concepts on the website and use synonyms or related phrases where appropriate to add variety. "
            f"Avoid using the website's brand name or overly general terms like 'service,' 'product,' or 'information' in every question. "
            f"Phrase the questions as if a user needs specific help or information. Keep the questions short (maximum 7 words). "
            f"Avoid overly promotional or marketing-oriented language.\n\n"
            f"{content[:1000]}"
            )
    else:
        prompt = (
            f"Analyze the following website content and generate 10 concise SEO keywords (maximum 5 words each) that a user would likely use to find similar information or services. "
            f"Identify the main topics, user needs, and search intent. Instead of directly using terms from the website, brainstorm related keywords and synonyms that a user might search. "
            f"Provide keywords in a natural, conversational search phrase format, mimicking typical search engine queries. "
            f"Prioritize keywords that are relevant, varied, specific, and likely to attract a targeted audience. Avoid excessive repetition of words or phrases found directly on the website.\n\n"
            f"{content[:1000]}"
            )
        
        

    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
# ✅ Safe debug logging
    print("HF RESPONSE:", response.status_code)
    print("RAW TEXT:", response.text)
    if response.status_code != 200:
        return [{"keyword": "API error", "volume": "?", "competition": "?"}]

    try:
        output = response.json()[0]["generated_text"]
    except Exception:
        return [{"keyword": "Parsing error", "volume": "?", "competition": "?"}]

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
            entry = {"keyword": line}
            if mode == "seo":
                entry["volume"] = random.randint(100, 10000)
                entry["competition"] = random.choice(["Low", "Medium", "High"])
            else:
                entry["type"] = "geo"
            keywords.append(entry)

    if not keywords:
        keywords = [{"keyword": line.strip(), "volume": "?", "competition": "?"}
                    for line in output.split("\n") if line.strip()]

    return keywords

    


@app.route('/generate_keywords', methods=['POST'])
def generate_keywords():
    data = request.get_json()
    url = data.get('url')
    #industry = data.get('industry', 'general')
    mode = data.get('mode', 'seo')  # NEW: check if user wants geo or seo

    content = extract_text_from_url(url)
    if content.startswith("Error"):
        return jsonify({"error": content}), 400

    keywords = generate_keywords_with_ai(content, mode=mode)  # pass mode here
    return jsonify(keywords)


if __name__ == '__main__':
    app.run(debug=True)
