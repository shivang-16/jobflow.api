
from function.utils import createFile, fetch_job_salary
from function.insert_job import insert_job
async def scrape_glassdoor(soup):
    portal = 'glassdoor'
    job_list = soup.find('ul', class_='JobsList_jobsList__lqjTr')
    print("here is pointer -1", job_list)
    if job_list:
        jobs = job_list.find_all('li')
        with open(f"{portal}_jobs.txt", "w", encoding="utf-8") as file:
            print("here is pointer 0")
            for job in jobs:
                title = job.find('a', class_='JobCard_jobTitle___7I6y')
                company_name = job.find('span', class_='EmployerProfile_compactEmployerName__LE242')
                job_link = title['href'] if title else None
                job_location = job.find('div', class_='JobCard_location__rCz3x')
                job_salary = job.find('div', class_='JobCard_salaryEstimate__arV5J')

                createFile(file, title, company_name, job_link, job_location, job_salary)
                print("here is pointer 1")
                if title and company_name and job_link and job_location:
                    print("here is pointer 2")
                    job_info = {
                        "title": title.text.strip(),
                        "company_name": company_name.text.strip(),
                        "job_link": f"https://www.glassdoor.co.in{job_link}",
                        "job_location": job_location.text.strip(),
                        "job_salary": job_salary.text.strip() if job_salary else None,
                        "source": portal
                    }
                    print("here is pointer 3")
                    try:
                        print("Inserting job data:", job_info)  # Debugging log
                        await insert_job(job_info)
                        print("Insert successful for:", job_info["title"])
                    except Exception as e:
                        print(f"Error inserting job for {job_info.get('title', 'unknown')}: {e}")
