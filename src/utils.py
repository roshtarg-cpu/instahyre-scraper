"""Utility functions for proxy handling and page fetching."""

import os
from urllib.parse import urlparse


def _parse_proxy(proxy_url):
    """Parse proxy URL into components for Camoufox."""
    if not proxy_url:
        return None
    
    parsed = urlparse(proxy_url)
    return {
        "server": f"{parsed.scheme}://{parsed.hostname}:{parsed.port}",
        "username": parsed.username,
        "password": parsed.password,
    }


async def _fetch(page, url, timeout=90000):
    """Fetch a URL with Camoufox page, handle Cloudflare challenges."""
    try:
        response = await page.goto(
            url,
            wait_until="networkidle",
            timeout=timeout
        )
        
        # Wait extra time for Cloudflare challenge to complete
        await page.wait_for_timeout(3000)
        
        content = await page.content()
        
        # Check if we got blocked
        if len(content) < 500:
            return None
        
        if "challenge" in content.lower() or "just a moment" in content.lower():
            # Wait longer for Cloudflare
            await page.wait_for_timeout(5000)
            content = await page.content()
        
        return content
    
    except Exception as e:
        print(f"Fetch error for {url}: {e}")
        return None
