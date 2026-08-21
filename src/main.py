"""Main actor logic."""

import asyncio
from datetime import datetime, timezone
from apify import Actor
from camoufox.async_api import AsyncCamoufox
from .utils import _parse_proxy, _fetch
from .parser import _extract_jobs_from_page


async def main():
    """Main actor entry point."""
    async with Actor:
        Actor.log.info("🚀 Instahyre Scraper starting...")
        
        # Get input
        actor_input = await Actor.get_input() or {}
        search_query = actor_input.get('searchQuery', 'python developer')
        location = actor_input.get('location', 'Bangalore')
        min_exp = actor_input.get('minExperience', 0)
        max_exp = actor_input.get('maxExperience', 10)
        max_results = actor_input.get('maxResults', 50)
        proxy_config = actor_input.get('proxyConfiguration', {})
        
        Actor.log.info(f"Search: '{search_query}' in {location} ({min_exp}-{max_exp} years exp)")
        Actor.log.info(f"Target: {max_results} jobs")
        
        # Get proxy URL
        proxy_url = None
        if proxy_config.get('useApifyProxy'):
            proxy_url = Actor.create_proxy_url(
                proxy_configuration=proxy_config,
                session=f"instahyre_{search_query.replace(' ', '_')}"
            )
            Actor.log.info(f"Using proxy: {proxy_url[:50]}...")
        
        proxy_settings = _parse_proxy(proxy_url)
        
        # Build search URL
        # Instahyre URL pattern: /search-jobs/?q=query&l=location
        search_url = f"https://www.instahyre.com/search-jobs/?q={search_query.replace(' ', '+')}"
        if location and location.lower() != 'any':
            search_url += f"&l={location.replace(' ', '+')}"
        
        Actor.log.info(f"Starting scrape: {search_url}")
        
        all_jobs = []
        page_num = 1
        max_pages = 10  # Safety limit
        
        # Launch Camoufox browser
        async with AsyncCamoufox(
            headless=True,
            geoip=True,
            humanize=True,
            proxy=proxy_settings
        ) as browser:
            page = await browser.new_page()
            
            while len(all_jobs) < max_results and page_num <= max_pages:
                Actor.log.info(f"📄 Fetching page {page_num}...")
                
                # Build paginated URL
                current_url = search_url
                if page_num > 1:
                    current_url += f"&page={page_num}"
                
                # Retry logic
                html = None
                for attempt in range(3):
                    html = await _fetch(page, current_url)
                    if html:
                        break
                    Actor.log.warning(f"Attempt {attempt + 1}/3 failed, retrying...")
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                
                if not html:
                    Actor.log.error(f"Failed to fetch page {page_num} after 3 attempts")
                    break
                
                # Parse jobs from page
                jobs = _extract_jobs_from_page(html)
                
                if not jobs:
                    Actor.log.info("No more jobs found, stopping pagination")
                    break
                
                Actor.log.info(f"Found {len(jobs)} jobs on page {page_num}")
                
                # Add timestamp and push to dataset
                now = datetime.now(timezone.utc).isoformat()
                for job in jobs:
                    if len(all_jobs) >= max_results:
                        break
                    
                    job['scrapedAt'] = now
                    
                    # Ensure all fields exist (use None for missing)
                    for field in ['jobTitle', 'companyName', 'location', 'salary', 
                                  'experience', 'skills', 'jobDescription', 'applyUrl', 'postedDate']:
                        if field not in job:
                            job[field] = None
                    
                    await Actor.push_data(job)
                    all_jobs.append(job)
                
                Actor.log.info(f"Progress: {len(all_jobs)}/{max_results} jobs scraped")
                
                page_num += 1
                await asyncio.sleep(2)  # Polite delay between pages
        
        Actor.log.info(f"✅ Scraping complete! Total jobs: {len(all_jobs)}")
        Actor.log.info(f"Dataset: {len(all_jobs)} items")


if __name__ == "__main__":
    asyncio.run(main())
