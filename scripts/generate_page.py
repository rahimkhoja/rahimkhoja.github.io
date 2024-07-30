import openai
import os

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def format_repo_with_gpt(repo):
    prompt = f"""
    Format the following repository information into a nice HTML block with proper styling:

    Name: {repo['name']}
    URL: {repo['html_url']}
    Description: {repo['description']}
    Tags: {', '.join(repo['tags'])}

    HTML:
    """
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7
    )
    return response.choices[0].text.strip()

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

        # Get formatted HTML from GPT
        formatted_html = format_repo_with_gpt(repo)
        formatted_repos += f"<div class='repo'>{formatted_html}</div>\n"

with open("docs/index.html", "r") as f:
    html_template = f.read()

html_content = html_template.replace("<!-- Repositories will be inserted here -->", formatted_repos)

with open("docs/index.html", "w") as f:
    f.write(html_content)

