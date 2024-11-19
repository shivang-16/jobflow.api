from function.utils import createFile, scrape_job_link
from function.insert_job import insert_job

async def scrape_ycombinator(soup):
    portal = 'ycombinator'
    # Locate all job entries
    jobs = soup.find_all('div', class_='w-full bg-beige-lighter mb-2 rounded-md p-2 border border-gray-200 flex')

    if jobs:
        with open(f"{portal}_jobs.txt", "w", encoding="utf-8") as file:
            for job in jobs:
                # Extract job title
                title_tag = job.find('div', class_='job-name').find('a')
                title = title_tag.text.strip() if title_tag else None

                # Extract job link
                job_link = title_tag['href'] if title_tag and 'href' in title_tag.attrs else None

                # Extract job location
                job_details = job.find('p', class_='job-details')
                if job_details:
                    spans = job_details.find_all('span')
                    if len(spans) > 1:  # Ensure there are at least two spans
                        job_location = spans[1].text.strip()  # Extract text from the second span
                    else:
                        job_location = "Not specified"  # Fallback if the second span doesn't exist
                else:
                    job_location = "Not specified"
                
                company_name = job.find('div', class_='company-details').find('span')
                company_logo_element = job.find('div', class_='company-logo')
                company_logo = None
                if company_logo_element:
                    img_tag = company_logo_element.find('img')
                    if img_tag:
                        company_logo = img_tag['src']

                job_details = await scrape_job_link(job_link, portal)
                job_salary=None
                if job_details:
                    job_salary_element = job_details.find('div', class_="company-title")
                    if job_salary_element:
                        job_salary = job_salary_element.find('div', class_='text-gray-500 my-2').find('span').text.strip()
                        print(job_salary)

                # Construct job info dictionary
                job_info = {
                    "title": title,
                    "job_link": job_link,
                    "job_location": job_location,
                    "company_name": company_name.text.strip() if company_name else None,
                    "company_logo": company_logo,
                    "job_salary": job_salary,
                    "source": portal
                }

                print(job_info, "here")

                # Insert the job info into the database
                await insert_job(job_info)

            