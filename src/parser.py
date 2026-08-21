"""HTML parsing functions to extract job data."""

from bs4 import BeautifulSoup
import re


def _extract_jobs_from_page(html, base_url="https://www.instahyre.com"):
    """Extract job listings from Instahyre search results page."""
    if not html or len(html) < 1000:
        return []
    
    soup = BeautifulSoup(html, 'html.parser')
    jobs = []
    
    # Instahyre uses various class patterns for job cards
    # We'll try multiple selectors
    job_cards = soup.find_all('div', class_=lambda x: x and ('job-card' in x.lower() or 'opportunity-card' in x.lower()))
    
    if not job_cards:
        # Fallback: look for links containing /job/
        job_links = soup.find_all('a', href=re.compile(r'/job/\d+'))
        job_cards = [link.find_parent(['div', 'article']) for link in job_links if link.find_parent(['div', 'article'])]
    
    for card in job_cards:
        if not card:
            continue
            
        try:
            job = _parse_job_card(card, base_url)
            if job and job.get('jobTitle') and job.get('applyUrl'):
                jobs.append(job)
        except Exception as e:
            print(f"Error parsing job card: {e}")
            continue
    
    return jobs


def _parse_job_card(card, base_url):
    """Parse a single job card into structured data."""
    job = {}
    
    # Job title - usually in h2, h3, or strong tag, or in a link
    title_elem = card.find(['h2', 'h3', 'strong', 'a'], class_=lambda x: x and 'title' in x.lower()) if card else None
    if not title_elem:
        title_elem = card.find('a', href=re.compile(r'/job/'))
    job['jobTitle'] = title_elem.get_text(strip=True) if title_elem else None
    
    # Company name
    company_elem = card.find(class_=lambda x: x and 'company' in x.lower())
    job['companyName'] = company_elem.get_text(strip=True) if company_elem else None
    
    # Location
    location_elem = card.find(class_=lambda x: x and 'location' in x.lower())
    if not location_elem:
        location_elem = card.find(string=re.compile(r'Bangalore|Mumbai|Delhi|Hyderabad|Pune|Chennai|Remote', re.I))
    job['location'] = location_elem.get_text(strip=True) if location_elem and hasattr(location_elem, 'get_text') else str(location_elem) if location_elem else None
    
    # Salary
    salary_elem = card.find(class_=lambda x: x and ('salary' in x.lower() or 'ctc' in x.lower()))
    if not salary_elem:
        salary_elem = card.find(string=re.compile(r'₹.*L|Lakh|LPA', re.I))
    job['salary'] = salary_elem.get_text(strip=True) if salary_elem and hasattr(salary_elem, 'get_text') else str(salary_elem) if salary_elem else None
    
    # Experience
    exp_elem = card.find(class_=lambda x: x and 'experience' in x.lower())
    if not exp_elem:
        exp_elem = card.find(string=re.compile(r'\d+\s*-\s*\d+\s*years?', re.I))
    job['experience'] = exp_elem.get_text(strip=True) if exp_elem and hasattr(exp_elem, 'get_text') else str(exp_elem) if exp_elem else None
    
    # Skills - usually in multiple span/badge elements
    skill_container = card.find(class_=lambda x: x and ('skill' in x.lower() or 'tag' in x.lower() or 'badge' in x.lower()))
    if skill_container:
        skills = [s.get_text(strip=True) for s in skill_container.find_all(['span', 'a', 'div'])]
        job['skills'] = ', '.join(skills) if skills else None
    else:
        job['skills'] = None
    
    # Job description - truncated from card or fetch from detail page
    desc_elem = card.find(class_=lambda x: x and 'description' in x.lower())
    job['jobDescription'] = desc_elem.get_text(strip=True)[:500] if desc_elem else None
    
    # Apply URL
    link_elem = card.find('a', href=re.compile(r'/job/'))
    if link_elem and link_elem.get('href'):
        href = link_elem['href']
        job['applyUrl'] = href if href.startswith('http') else f"{base_url}{href}"
    else:
        job['applyUrl'] = None
    
    # Posted date
    date_elem = card.find(class_=lambda x: x and ('date' in x.lower() or 'time' in x.lower() or 'posted' in x.lower()))
    if not date_elem:
        date_elem = card.find(string=re.compile(r'\d+\s*(day|hour|week|month)s?\s*ago', re.I))
    job['postedDate'] = date_elem.get_text(strip=True) if date_elem and hasattr(date_elem, 'get_text') else str(date_elem) if date_elem else None
    
    return job
