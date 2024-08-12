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
        if repo["description"]:  # Skip repos without descriptions
            repo_info = {
                "name": repo["name"],
                "html_url": repo["html_url"],
                "description": repo["description"],
                "tags": repo["topics"] if "topics" in repo else [],
                "homepage": repo["homepage"],
                "stargazers_count": repo["stargazers_count"],
                "forks_count": repo["forks_count"],
                "language": repo["language"]
            }
            all_repos.append(repo_info)

# Save repo info to a markdown file
with open("repos.md", "w") as f:
    for repo in all_repos:
        tags = ', '.join(repo['tags'])
        f.write(f"### [{repo['name']}]({repo['html_url']})\n{repo['description']}\n**Tags**: {tags}\n\n")
