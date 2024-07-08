import json
import re

def parse_resume(resume_text):
    # Initialize dictionary to store parsed data
    parsed_data = {
        "personal_info": {},
        "education": [],
        "experience": [],
        "skills": [],
        "publications": []
    }

    # Extract personal information
    name_match = re.search(r'^(.+?)(?=\n)', resume_text)
    if name_match:
        parsed_data["personal_info"]["name"] = name_match.group(1).strip()

    contact_info = re.search(r'(.+?)\n(.+?)\n(.+)', resume_text)
    if contact_info:
        parsed_data["personal_info"]["address"] = contact_info.group(1).strip()
        parsed_data["personal_info"]["phone"] = contact_info.group(2).strip()
        parsed_data["personal_info"]["email"] = contact_info.group(3).strip()

    # Extract education
    education_section = re.search(r'Education(.*?)Experience', resume_text, re.DOTALL)
    if education_section:
        education_items = re.findall(r'(.+?)\n(.+?)\n(.+?)\n', education_section.group(1))
        for item in education_items:
            parsed_data["education"].append({
                "degree": item[0].strip(),
                "institution": item[1].strip(),
                "details": item[2].strip()
            })

    # Extract experience
    experience_section = re.search(r'Experience(.*?)Publications', resume_text, re.DOTALL)
    if experience_section:
        experience_items = re.split(r'\n(?=\S)', experience_section.group(1).strip())
        for item in experience_items:
            parts = item.split('\n', 2)
            if len(parts) >= 3:
                parsed_data["experience"].append({
                    "title": parts[0].strip(),
                    "date": parts[1].strip(),
                    "details": parts[2].strip()
                })

    # Extract skills
    skills_section = re.search(r'Technical Skills(.*?)$', resume_text, re.DOTALL)
    if skills_section:
        skills = re.findall(r'•\s*(.+)', skills_section.group(1))
        parsed_data["skills"] = [skill.strip() for skill in skills]

    # Extract publications
    publications_section = re.search(r'Publications(.*?)Technical Skills', resume_text, re.DOTALL)
    if publications_section:
        publications = re.findall(r'•\s*(.+)', publications_section.group(1))
        parsed_data["publications"] = [pub.strip() for pub in publications]

    return parsed_data

# Read the resume text
with open('resume.txt', 'r') as file:
    resume_text = file.read()

# Parse the resume
parsed_resume = parse_resume(resume_text)

# Convert to JSON
json_output = json.dumps(parsed_resume, indent=2)

# Print or save the JSON output
print(json_output)

# Optionally, save to a file
with open('parsed_resume.json', 'w') as json_file:
    json_file.write(json_output)
