
import requests
from bs4 import BeautifulSoup

# Function to extract visible text from a webpage
def extract_text_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = ' '.join([p.get_text() for p in soup.find_all(['p', 'h1', 'h2', 'h3'])])
        return text[:3000]  # Limit for testing
    except Exception as e:
        return f"Error: {e}"

# Mocked AI keyword generation (replace with LLaMA/OpenAI later)
def generate_keywords_with_ai(content, industry):
    return [
        {"keyword": "best seo tools for small businesses", "volume": 1000, "competition": "Low"},
        {"keyword": "how to rank on google in 2024", "volume": 880, "competition": "Medium"},
        {"keyword": "seo keyword research for beginners", "volume": 720, "competition": "Medium"},
        {"keyword": "long tail keywords example", "volume": 600, "competition": "Low"},
        {"keyword": "free seo audit tools", "volume": 500, "competition": "High"}
    ]

# Example usage
if __name__ == '__main__':
    test_url = 'https://example.com'
    test_industry = 'marketing'

    print(f"Extracting text from {test_url}...")
    content = extract_text_from_url(test_url)
    print("Website content preview:")
    print(content[:500], '\n...\n')

    print("Generating keywords:")
    results = generate_keywords_with_ai(content, test_industry)
    for item in results:
        print(f"{item['keyword']} | Volume: {item['volume']} | Competition: {item['competition']}")
