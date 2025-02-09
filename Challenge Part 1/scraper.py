# scraper.py
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import sys

def scrape_professors(url, faculty_type):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch the webpage: {url}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    profiles_container = soup.find(class_="entry-content directory-profiles")
    if not profiles_container:
        print("Could not find professor profiles.")
        return []

    professor_profiles = profiles_container.find_all(class_="ecs-profile box-clickable")
    data = []
    total_profiles = len(professor_profiles)
    for i, profile in enumerate(professor_profiles):
        print(f"Processing {faculty_type} faculty: {i+1}/{total_profiles}...", end="\r")
        sys.stdout.flush()

        name_tag = profile.find(class_="profile-name").find("a")
        title_tag = profile.find(class_="profile-title")

        if name_tag:
            name = name_tag.text.strip()
            link = name_tag.get("href", "")
            title = title_tag.text.strip() if title_tag else ""
            interests, description, current_research, publications = scrape_interests_description_research_publications(link) if link else ("", "", "", "")
            data.append([name, link, title, interests, description, current_research, publications])

    print(f"Processed {total_profiles} {faculty_type} faculty profiles.")
    return data

def scrape_interests_description_research_publications(professor_url):
    response = requests.get(professor_url)
    if response.status_code != 200:
        return "", "", "", ""

    soup = BeautifulSoup(response.text, 'html.parser')
    interests, description, current_research, publications = [], [], [], []
    interest_section_found, research_section_found, publications_section_found = False, False, False
    time.sleep(0.1)

    for heading in soup.find_all("p"):
        if heading.find("strong") and ("Areas of Expertise:" in heading.text or "Research Interests:" in heading.text):
            interest_section_found = True
            for ul in heading.find_next_siblings("ul", class_="wp-block-list"):
                interests.extend([li.text.strip() for li in ul.find_all("li")])
        elif interest_section_found:
            if heading.name == "p" and len(heading.text.split()) > 5:
                description.append(heading.text.strip())
            else:
                interest_section_found = False
        if heading.find("strong") and "Current Research:" in heading.text:
            research_section_found = True
        elif research_section_found:
            if heading.name == "p" and len(heading.text.split()) > 5:
                current_research.append(heading.text.strip())
            else:
                research_section_found = False
        if heading.find("strong") and ("Selected Presentations/Publications:" in heading.text or "Select Publications:" in heading.text or "Selected Publications:" in heading.text):
            publications_section_found = True
            for ul in heading.find_next_siblings("ul", class_="wp-block-list"):
                publications.extend([li.text.strip() for li in ul.find_all("li")])
        elif publications_section_found:
            if heading.name == "p" and len(heading.text.split()) > 5:
                publications.append(heading.text.strip())
            else:
                break

    return "; ".join(interests), " ".join(description), " ".join(current_research), " ".join(publications)


def scrape_and_save_professors(professors_file):
    """Scrapes professor data and saves it to an Excel file."""
    full_time_url = "https://ecs.syracuse.edu/faculty-staff?category=full-time-fac&people="
    part_time_url = "https://ecs.syracuse.edu/faculty-staff?category=part-time-fac&people="
    data = scrape_professors(full_time_url, "Full-Time") + scrape_professors(part_time_url, "Part-Time")
    df = pd.DataFrame(data, columns=["Professor Name", "Link", "Profile Title", "Areas of Interest / Research Interests", "Description", "Current Research", "Publications"])
    df.to_excel(professors_file, index=False, engine='openpyxl')  # Specify engine
    print(f"Professor data saved to {professors_file}")


if __name__ == '__main__':
    # Example usage (you can run this directly to test the scraper):
    scrape_and_save_professors('professors.xlsx')