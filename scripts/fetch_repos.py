import requests

# List of GitHub usernames
usernames = ["rahimkhoja", "ImprobabilityLabs"]

# Get repos for each user
def get_repos(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    return response.json()

# Fetch repos and save info
all_repos = []
for username in usernames:
    repos = get_repos(username)
    for repo in repos:
        repo_info = {
            "name": repo["name"],
            "html_url": repo["html_url"],
            "description": repo["description"] or "No description available.",
            "tags": repo["topics"] if "topics" in repo else []
        }
        all_repos.append(repo_info)

# Save repo info to a markdown file
with open("repos.md", "w") as f:
    for repo in all_repos:
        tags = ', '.join(repo['tags'])
        f.write(f"### [{repo['name']}]({repo['html_url']})\n{repo['description']}\n**Tags**: {tags}\n\n")

