import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from function.crawler.job_portals import (
    scrape_glassdoor,
    scrape_linkedin,
    scrape_simplyhired,
    scrape_indeed,
    scrape_upwork,
    scrape_freelancer,
    scrape_internshala
)
import os

load_dotenv()

scraperapi_key = os.getenv('SCRAPER_API')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}


searchKeyword = 'Web developer'

jobPortals = {
    "glassdoor": f"https://www.glassdoor.co.in/Job/{searchKeyword}-jobs-SRCH_KO0,16.htm",
    "linkedin": f"https://www.linkedin.com/jobs/search?keywords={searchKeyword}",
    "simplyhired": f"https://www.simplyhired.co.in/search?q={searchKeyword}",
    "indeed": f"https://in.indeed.com/jobs?q={searchKeyword}",
    "foundit": f"https://www.foundit.in/srp/results?query={searchKeyword}",
    "naukri": f"https://www.naukri.com/{searchKeyword}-jobs?k={searchKeyword}",
    "internshala": f"https://internshala.com/jobs/{searchKeyword}-jobs/",
    "ycombinator": f"https://www.workatastartup.com/companies?query={searchKeyword}&sortBy=keyword",
    "upwork": f"https://www.upwork.com/nx/search/jobs/?q={searchKeyword}",
    "freelancer": f"https://www.freelancer.com/search/projects?q={searchKeyword}",
}
    

async def scrapejobsdata():
    for portal, url in jobPortals.items():
        print(f"Scraping {portal}: {url}")

        try:
            if portal == 'linkedin':
                response = requests.get(url, headers=headers)
                print(response, "here")
            else:
                proxy_url = f"http://api.scraperapi.com?api_key={scraperapi_key}&url={url}"
                response = requests.get(proxy_url, headers=headers)

            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            with open(f"{portal}.html", "w", encoding="utf-8") as file:
                file.write(soup.prettify())

            print("success")

            if portal == 'linkedin':
                print("here")
                await scrape_linkedin(soup)

            elif portal == 'glassdoor':
                print("here is pointer -2")
                await scrape_glassdoor(soup)

            elif portal == 'indeed':
                await scrape_indeed(soup)

            elif portal == 'internshala':
                await scrape_internshala(soup)

            elif portal == 'simplyhired':
                await scrape_simplyhired(soup)

            elif portal == 'upwork':
                await scrape_upwork(soup)

            elif portal == 'freelancer':
                await scrape_freelancer(soup)

        except requests.exceptions.RequestException as e:
            print(f"Failed to scrape {portal}: {e}")

