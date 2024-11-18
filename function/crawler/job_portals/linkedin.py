from function.utils import createFile, fetch_job_salary
from function.insert_job import insert_job
async def scrape_linkedin(soup):
     portal = 'linkedin'
     job_list = soup.find('ul', class_='jobs-search__results-list')
     if job_list:
        jobs = job_list.find_all('li')
        with open(f"{portal}_jobs.txt", "w", encoding="utf-8") as file:
            for job in jobs:
                title = job.find('h3', class_='base-search-card__title')
                company_name = job.find('h4', class_='base-search-card__subtitle')
                job_link = job.find('a', class_='base-card__full-link')
                job_location = job.find('span', class_='job-search-card__location')
                job_salary = fetch_job_salary(job_link['href'].strip()) if job_link else None
                company_logo_element = job.find('div', class_='search-entity-media')
                company_logo=None
                if company_logo_element:
                    img_tag= company_logo_element.find('img')
                    if img_tag: 
                        company_logo = img_tag['data-delayed-url']

                print(company_logo, "here is company log")

                if title and company_name and job_link and job_location:
                    job_info = {
                        "title": title.text.strip(),
                        "company_name": company_name.text.strip(),
                        "company_logo": company_logo,
                        "job_link": job_link['href'].strip(),
                        "job_location": job_location.text.strip(),
                        "job_salary": job_salary,
                        "source": portal,
                    }
                    # job_data.append(job_info)
                    try:
                        print("Inserting job data:", job_info)  # Debugging log
                        await insert_job(job_info)
                        print("Insert successful for:", job_info["title"])
                    except Exception as e:
                        print(f"Error inserting job for {job_info.get('title', 'unknown')}: {e}")
                    
