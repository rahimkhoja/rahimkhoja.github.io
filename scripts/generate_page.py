with open("repos.md", "r") as f:
    repos_content = f.read()

with open("docs/index.html", "r") as f:
    html_template = f.read()

html_content = html_template.replace("<!-- Repositories will be inserted here -->", repos_content)

with open("docs/index.html", "w") as f:
    f.write(html_content)

