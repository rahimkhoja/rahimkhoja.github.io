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


html_output = ""

color_classes = ["color1", "color2", "color3", "color4", "color5"]
color_index = 0

for repo in all_repos:
    tags_html = ""
    for tag in repo["tags"]:
        color_class = color_classes[color_index % len(color_classes)]
        tags_html += f'          <a title="" href="" class="{color_class}">{tag}</a>\n'
        color_index += 1

    repo_html = f"""
          <div class="col-md-12 mt-4 mt-md-0 icon-box" data-aos="fade-up" data-aos-delay="100">
            <h4 style="text-align:left;">{repo["name"]}</h4>
            <p>{repo["description"]}</p>
            
            <div class="repo-links mt-3">
              <div class="github-repo">
                <strong>Repository:</strong>
                <a href="{repo["html_url"]}" target="_blank">{repo["html_url"]}</a>
              </div>
    """
    
    if repo["homepage"]:
        repo_html += f"""
              <div class="demo mt-2">
                <strong>Live Demo:</strong>
                <a href="{repo["homepage"]}" target="_blank">{repo["homepage"]}</a>
              </div>
        """
    
    repo_html += f"""
            </div>
    
            <div class="repo-stats mt-3">
              <span class="mr-3">
                <i class="bx bx-star"></i> {repo["stargazers_count"]}
              </span>
              <span>
                <i class="bx bx-git-branch"></i> {repo["forks_count"]}
              </span>
            </div>
    
            <div class="tags mt-3">
              <p>
    {tags_html}
              </p>
            </div>
          </div>
    """
    
    html_output += repo_html

# Print the final HTML output
print(html_output)

# Save repo info to a markdown file
with open("docs\repos.html", "w") as f:
    f.write(html_output)

# Save repo info to a markdown file
with open("repos.md", "w") as f:
    for repo in all_repos:
        tags = ', '.join(repo['tags'])
        f.write(f"### [{repo['name']}]({repo['html_url']})\n{repo['description']}\n**Tags**: {tags}\n\n")
