from function.utils import createFile, fetch_job_salary
from function.insert_job import insert_job
async def scrape_indeed(soup):
    portal = 'indeed'
    job_list = soup.find('ul', class_='css-1faftfv')
    if job_list:
        jobs = job_list.find_all('li')
        with open(f"{portal}_jobs.txt", "w", encoding="utf-8") as file:

            for job in jobs:
                company_name_element = job.find('span', class_='css-1h7lukg eu4oa1w0')
                job_location_element = job.find('div', class_='css-1restlb eu4oa1w0')
                # job_salary_element = job.find('div', class_='salary-snippet-container')
                job_link_element = job.find('a', class_='jcs-JobTitle')
                if job_link_element:
                    job_link = f"https://in.indeed.com{job_link_element['href']}"
                    title_element = job_link_element.find('span')
                
                    
                    print("before create file", company_name_element, job_link, )
                    createFile(file, title_element.text.strip(), company_name_element.text.strip(), job_link, job_location_element.text.strip())

                    if title_element and company_name_element and job_location_element:
                        job_info = {
                            "title": title_element.text.strip(),
                            "company_name": company_name_element.text.strip(),
                            "job_link": job_link,
                            "job_location": job_location_element.text.strip(),
                            "job_salary":  None,
                            "source": portal
                        }
                        try:
                            print("Inserting job data:", job_info)  # Debugging log
                            await insert_job(job_info)
                            print("Insert successful for:", job_info["title"])
                        except Exception as e:
                            print(f"Error inserting job for {job_info.get('title', 'unknown')}: {e}")
