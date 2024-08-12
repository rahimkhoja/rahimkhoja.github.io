import yaml

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
              <figure class="item" style="display:inline-block;">
                <a href="{skill['link']}" target="_blank" rel="noreferrer">
                  <img src="{skill['icon']}" alt="{skill['name']}" width="40" height="40" />
                </a>
                <figcaption style="text-align:center;">{skill['name']}</figcaption>
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
    resume = data['resume']
    projects = data['projects']

    name = personal_info.get('name')
    email = personal_info.get('email')
    linkedin = personal_info.get('linkedin')
    stackoverflow = personal_info.get('stackoverflow')
    github = personal_info.get('github')
    hackerrank = personal_info.get('hackerrank')
    leetcode = personal_info.get('leetcode')
    researchgate = personal_info.get('researchgate')
    about = personal_info.get('about')

    skills_html = generate_html(skills)

    with open("docs/skills_section.html", "w") as f:
        f.write(skills_html)

    with open("docs/index2.html", "r") as f:
        html_template = f.read()

    html_template = html_template.replace("<!-- Skills -->", skills_html)
    html_template = html_template.replace("<!-- Name -->", name)
    html_template = html_template.replace("<!-- Email -->", email)
    html_template = html_template.replace("<!-- LinkedIn -->", linkedin)
    html_template = html_template.replace("<!-- Stack -->", stackoverflow)
    html_template = html_template.replace("<!-- GitHub -->", github)
    html_template = html_template.replace("<!-- HackerRank -->", hackerrank)
    html_template = html_template.replace("<!-- LeetCode -->", leetcode)
    html_template = html_template.replace("<!-- ResearchGate -->", researchgate)
    html_template = html_template.replace("<!-- About -->", about)

    with open("docs/index2.html", "w") as f:
        f.write(html_template)
