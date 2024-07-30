with open("repos.md", "r") as f:
    repos_content = f.read()

repo_items = repos_content.split("\n\n")

formatted_repos = ""
for item in repo_items:
    if item.strip():
        formatted_repos += f'<div class="repo">{item.replace("### ", "<h3>").replace("\n", "</h3><p>").replace("\n**Tags**: ", "<br><strong>Tags:</strong> ").replace("</h3><p>", "</h3><p>")}</p></div>\n'

with open("docs/index.html", "r") as f:
    html_template = f.read()

html_content = html_template.replace("<!-- Repositories will be inserted here -->", formatted_repos)

with open("docs/index.html", "w") as f:
    f.write(html_content)

