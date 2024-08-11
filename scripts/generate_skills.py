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
    
    with open("docs/skills_section.html", "w") as f:
        f.write(html)

if __name__ == "__main__":
    with open("details.json", "r") as stream:
        skills_data = yaml.safe_load(stream)['skills']
    generate_html(skills_data)

