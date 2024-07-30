import requests
import os
from html.parser import HTMLParser

# Set your GroqCloud API key
GROQ_KEY = os.getenv("GROQ_KEY")

class HTMLValidator(HTMLParser):
    def __init__(self):
        super().__init__()
        self.errors = []

    def handle_starttag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass

    def error(self, message):
        self.errors.append(message)

def validate_html(html):
    validator = HTMLValidator()
    validator.feed(html)
    return len(validator.errors) == 0

def format_repo_with_groq(repo):
    api_url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {GROQ_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""
    Format the following repository information into a nice HTML block with proper styling. Output only the HTML content without any additional notes or markup symbols.

    Example HTML:
    <div class="repo">
        <h2><a href="REPO_URL" target="_blank">REPO_NAME</a></h2>
        <p>REPO_DESCRIPTION</p>
        <p><strong>Tags:</strong> TAG_LIST</p>
    </div>

    Replace REPO_URL, REPO_NAME, REPO_DESCRIPTION, and TAG_LIST with the respective repository information.

    Name: {repo['name']}
    URL: {repo['html_url']}
    Description: {repo['description']}
    Tags: {', '.join(repo['tags'])}

    HTML:
    """
    
    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {
                "role": "system",
                "content": "Format the repository information into a nice HTML block."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 500,
        "top_p": 1,
        "stream": False,
        "stop": None
    }
    
    response = requests.post(api_url, headers=headers, json=payload)
    response.raise_for_status()
    
    response_json = response.json()
    formatted_html = response_json['choices'][0]['message']['content']
    
    if not validate_html(formatted_html):
        raise ValueError("Generated HTML is not valid")
    
    return formatted_html

with open("repos.md", "r") as f:
    repos_content = f.read()

repo_items = repos_content.strip().split("\n\n")

formatted_repos = ""
for item in repo_items:
    if item.strip():
        # Extract repo details
        name = item.split("\n")[0].split("](")[0].replace("### [", "")
        url = item.split("\n")[0].split("](")[1].replace(")", "")
        description = item.split("\n")[1]
        tags = item.split("**Tags**: ")[1] if "**Tags**: " in item else ""

        repo = {
            "name": name,
            "html_url": url,
            "description": description,
            "tags": tags.split(", ") if tags else []
        }

        # Get formatted HTML from GroqCloud
        formatted_html = format_repo_with_groq(repo)
        formatted_repos += f"<div class='repo'>{formatted_html}</div>\n"

with open("docs/index.html", "r") as f:
    html_template = f.read()

html_content = html_template.replace("<!-- Repositories will be inserted here -->", formatted_repos)

with open("docs/index.html", "w") as f:
    f.write(html_content)

