from function.utils import createFile, fetch_job_salary
from function.insert_job import insert_job
from bs4 import BeautifulSoup

async def scrape_ycombinator(soup):
    portal = 'ycombinator'
    print('inside ycombinator')

    # Locate all job entries
    jobs = soup.find_all('div', class_='w-full bg-beige-lighter mb-2 rounded-md p-2 border border-gray-200 flex')

    if jobs:
        with open(f"{portal}_jobs.txt", "w", encoding="utf-8") as file:
            for job in jobs:
                # Extract job title
                title_tag = job.find('div', class_='job-name').find('a')
                title = title_tag.text.strip() if title_tag else None

                print("here is title_tag", title)

                # Extract job link
                job_link = title_tag['href'] if title_tag and 'href' in title_tag.attrs else None

                print("here is job", job_link)

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
                
                print(job_location, "here are joblocaiton")

                company_name = job.find('div', class_='company-details').find('span')

                # Construct job info dictionary
                job_info = {
                    "title": title,
                    "job_link": job_link,
                    "job_location": job_location,
                    "company_name": company_name.text.strip() if company_name else None, 
                    "job_salary": None,
                    "source": portal
                }

                # Insert the job info into the database
                await insert_job(job_info)

                # Save to file
                createFile(file, title, None, job_info["job_link"], job_location)
