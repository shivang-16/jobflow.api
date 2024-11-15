
from function.utils import createFile, fetch_job_salary
from function.insert_job import insert_job
async def scrape_freelancer(soup):
    portal = 'freelancer'
    job_list = soup.find('div', id='project-list')
    if job_list:
        jobs = job_list.find_all('div', class_="JobSearchCard-item")

        with open(f"{portal}_jobs.txt", "w", encoding="utf-8") as file:
            for job in jobs:
                title_element = job.find('a', class_='JobSearchCard-primary-heading-link')
                title = title_element.text.strip() if title_element else "No title"
                job_link = title_element['href'] if title_element else "No link"
                job_location = "Remote"

                job_info = {
                    "title": title,
                    "job_link": f"https://www.freelancer.com{job_link}",
                    "job_location": job_location,
                    "job_salary": None,
                    "source": portal
                }
                await insert_job(job_info)

                print(title, job_link, job_location)
                createFile(file, title, None, f"https://www.freelancer.com{job_link}", job_location)
