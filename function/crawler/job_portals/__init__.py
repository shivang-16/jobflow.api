# job_ports/__init__.py

# Import everything from individual job portal files
from .glassdoor import scrape_glassdoor
from .linkedin import scrape_linkedin
from .simplyhired import scrape_simplyhired
from .indeed import scrape_indeed
from .upwork import scrape_upwork
from .freelancer import scrape_freelancer
from .internshala import scrape_internshala
from .ycombinator import scrape_ycombinator

__all__ = ['scrape_glassdoor', 'scrape_linkedin', 'scrape_simplyhired', 'scrape_indeed', 'scrape_upwork', 'scrape_freelancer', 'scrape_internshala', 'scrape_ycombinator']

