import yaml
import requests

# Get repos for each user
def get_repos(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    return response.json()

def generate_repo_html(all_repos):
    html_output = ""
    color_classes = ["color1", "color2", "color3", "color4", "color5"]
    color_index = 0
    
    for repo in all_repos:
        tags_html = ""
        for tag in repo["tags"]:
            color_class = color_classes[color_index % len(color_classes)]
            tags_html += f'                  <a title="" href="" class="{color_class}">{tag}</a>\n'
            color_index += 1

        repo_html = f"""
              <div class="col-md-12 mt-4 mt-md-0 icon-box" data-aos="fade-up" data-aos-delay="100">
                <h4>{repo["name"]}</h4>
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

    return html_output


def remove_lines_containing_text(file_content, text_to_delete):
    # Split into lines
    lines = file_content.splitlines()
    
    # Filter out lines containing the specific text
    filtered_content = [line for line in lines if text_to_delete not in line]
    
    # Join the filtered lines back into a single string
    filtered_content_str = "\n".join(filtered_content)
    
    return filtered_content_str


def generate_html(skills):
    sections = []
    for category, items in skills.items():
        # Convert category names to match your HTML section headers
        if category == 'programming_languages':
            category_name = "Languages"
        elif category == 'operating_systems':
            category_name = "Operating Systems"
        elif category == 'infrastructure_and_cloud_technologies':
            category_name = "Technologies"
        elif category == 'libraries_and_frameworks':
            category_name = "Libraries"
        elif category == 'devops_and_tools':
            category_name = "DevOps & Tools"
        elif category == 'databases':
            category_name = "Databases"
        else:
            category_name = category.capitalize()

        section = f"""
          <div class="col-md-12 mt-4 mt-md-0 icon-box" data-aos="fade-up" data-aos-delay="100">
            <h4 style="text-align:left;color:#12d640;">{category_name}</h4>
            <div style="text-align:left;">"""
        
        for skill in items:
            section += f"""
              <figure class="item" style="display:inline-block; text-align:center; margin: 0;">
                <a href="{skill['link']}" target="_blank" rel="noreferrer">
                  <img width="48" height="48" src="{skill['icon']}" alt="{skill['name']}" style="display: block; margin: 0 auto;"/>
                </a>
                <figcaption style="text-align:center; margin-top: 5px;">{skill['name']}</figcaption>
              </figure>
              &nbsp; &nbsp;"""
        
        section += "</div></div>"
        sections.append(section)
    
    html = f"""
<section id="skills" class="services">
    <div class="container">
      <div class="section-title">
        <h2>Skills</h2>
      </div>
      <div class="row">
        <div class="col-lg-12" data-aos="fade-up">
          {"".join(sections)}
        </div>
      </div>
    </div>
  </section>"""

    return html 
    


if __name__ == "__main__":
    with open("scripts/details.yaml", "r") as stream:
        data = yaml.safe_load(stream)

    site_info = data['site_info']
    personal_info = data['personal_info']
    skills = data['skills']
    projects = data['projects']

    name = personal_info.get('name')
    email = personal_info.get('email')
    linkedin = personal_info.get('linkedin')
    stackoverflow = personal_info.get('stackoverflow')
    github = personal_info.get('github')
    hackerrank = personal_info.get('hackerrank')
    leetcode = personal_info.get('leetcode')
    researchgate = personal_info.get('researchgate')
    resume = personal_info.get('resume')
    typing_text = personal_info.get('typing_text')
    about = personal_info.get('about')

    # Assign the values site_info to variables
    bing = site_info.get('bing')
    google = site_info.get('google')
    gtag = site_info.get('gtag')
    page_title = site_info.get('page_title')
    meta_keywords = site_info.get('meta_keywords')
    page_description = site_info.get('page_description')

    skills_html = generate_html(skills)

    with open("scripts/html-template.html", "r") as f:
        html_template = f.read()

    # List of GitHub usernames
    usernames = ["rahimkhoja", "ImprobabilityLabs"]

    # Fetch repos and save info
    all_repos = []
    for username in usernames:
        repos = get_repos(username)
        for repo in repos:
            if repo["description"]:  # Skip repos without descriptions
                repo_info = {
                    "name": repo["name"].replace("_", " ").replace("-", " ").title(),
                    "html_url": repo["html_url"],
                    "description": repo["description"],
                    "tags": repo["topics"] if "topics" in repo else [],
                    "homepage": repo["homepage"],
                    "stargazers_count": repo["stargazers_count"],
                    "forks_count": repo["forks_count"],
                    "language": repo["language"]
                }
                all_repos.append(repo_info)

    repos_html = generate_repo_html(all_repos)
   
    html_template = html_template.replace("<!-- Skills -->", skills_html)
    html_template = html_template.replace("<!-- Repos -->", repos_html)
    
    if name:
        html_template = html_template.replace("<!-- Name -->", name)

    if email:
        html_template = html_template.replace("<!-- Email -->", email)

    if typing_text:
        html_template = html_template.replace("<!-- Typing_Text -->", typing_text)

    if resume:
        html_template = html_template.replace("<!-- Resume -->", resume)
    else:
        html_template = remove_lines_containing_text(html_template, "<!-- Resume -->")

    if about:
        html_template = html_template.replace("<!-- About -->", about)

    if linkedin:
        html_template = html_template.replace("<!-- LinkedIn -->", linkedin)
    else:
        html_template = remove_lines_containing_text(html_template, "<!-- LinkedIn -->")

    if stackoverflow:
        html_template = html_template.replace("<!-- Stack -->", stackoverflow)
    else:
        html_template = remove_lines_containing_text(html_template, "<!-- Stack -->")
        
    if github:
        html_template = html_template.replace("<!-- GitHub -->", github)
    else:
        html_template = remove_lines_containing_text(html_template, "<!-- GitHub -->")
        
    if hackerrank:
        html_template = html_template.replace("<!-- HackerRank -->", hackerrank)
    else:
        html_template = remove_lines_containing_text(html_template, "<!-- HackerRank -->")
        
    if leetcode:
        html_template = html_template.replace("<!-- LeetCode -->", leetcode)
    else:
        html_template = remove_lines_containing_text(html_template, "<!-- LeetCode -->")
    
    if researchgate:
        html_template = html_template.replace("<!-- ResearchGate -->", researchgate)
    else:
        html_template = remove_lines_containing_text(html_template, "<!-- ResearchGate -->")
        



    with open("docs/index2.html", "w") as f:
        f.write(html_template)
