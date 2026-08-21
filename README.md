# 🎯 Instahyre Jobs Scraper — India Tech Jobs for AI Agents

[![Apify](https://img.shields.io/badge/Apify-Actor-00C48C?logo=apify)](https://apify.com)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://python.org)
[![Camoufox](https://img.shields.io/badge/Browser-Camoufox-orange)](https://github.com/daijro/camoufox)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-purple)](https://modelcontextprotocol.io)

Extract **high-paying tech jobs from Instahyre.com** — India's premium platform for software engineers, data scientists, product managers, and tech professionals. Get job titles, salaries, skills, locations, and company details in structured JSON format.

Perfect for **AI agents** (Claude, ChatGPT, MCP integrations), recruitment automation, market intelligence, and salary benchmarking. Bypasses Cloudflare protection using stealth browser automation.

## 📊 What Data You Get

Each job listing includes:

| Field | Description |
|-------|-------------|
| `jobTitle` | Job position (e.g. "Senior Backend Engineer") |
| `companyName` | Hiring company name |
| `location` | Job location (city/region) |
| `salary` | Salary range (e.g. "₹25L - ₹40L/year") |
| `experience` | Required experience (e.g. "3-5 years") |
| `skills` | Required technologies/skills (Python, AWS, etc.) |
| `jobDescription` | Full job description text |
| `applyUrl` | Direct application URL |
| `postedDate` | When the job was posted |
| `scrapedAt` | ISO 8601 timestamp |

## 🎯 Features

✅ **Cloudflare Bypass** — Handles Cloudflare protection automatically  
✅ **Residential Proxies** — Uses Apify residential proxy rotation  
✅ **Search Filters** — Query by job title, location, experience level  
✅ **Pagination** — Scrapes multiple pages until `maxResults` reached  
✅ **Error Handling** — Retries failed requests, never crashes  
✅ **Structured Output** — Clean JSON compatible with any tool  
✅ **AI Agent Ready** — Works with Claude, ChatGPT via Apify MCP  

## 🚀 Quick Start

### Input Example

```json
{
  "searchQuery": "python developer",
  "location": "Bangalore",
  "minExperience": 2,
  "maxExperience": 5,
  "maxResults": 50,
  "proxyConfiguration": {
    "useApifyProxy": true,
    "apifyProxyGroups": ["RESIDENTIAL"]
  }
}
```

### Output Example

```json
{
  "jobTitle": "Senior Python Developer",
  "companyName": "Zomato",
  "location": "Bangalore, Karnataka",
  "salary": "₹20L - ₹35L per year",
  "experience": "3-5 years",
  "skills": ["Python", "Django", "PostgreSQL", "AWS", "Docker"],
  "jobDescription": "We are looking for an experienced Python developer...",
  "applyUrl": "https://www.instahyre.com/job/XXXXX",
  "postedDate": "2 days ago",
  "scrapedAt": "2026-08-21T14:23:45.123Z"
}
```

## 🤖 AI Integration

This actor works seamlessly with **AI agents and MCP servers**:

```
You: "Find Python jobs in India paying above 20 LPA"
Claude/ChatGPT: *calls Apify Instahyre actor*
→ Returns 50 matching jobs with salaries, skills, apply links
```

Compatible with:
- **Claude Desktop** + Apify MCP
- **ChatGPT** + Apify plugin
- **LangChain** / **AutoGPT** / **Crew AI**
- Any tool supporting Apify REST API

## 💰 Pricing

| Event | Price |
|-------|-------|
| Per job scraped | $0.005 |
| Actor start fee | $0.05 |

**Example:** Scraping 100 jobs = $0.50 + $0.05 start fee = **$0.55 total**

## 🔧 Advanced Configuration

### Proxy Settings

For best Cloudflare bypass, use **RESIDENTIAL** proxies (included in input example above).

### Search Filters

- `searchQuery`: Job title or skills (e.g. "machine learning", "devops engineer")
- `location`: City or region (e.g. "Mumbai", "Hyderabad", "Remote")
- `minExperience` / `maxExperience`: Filter by years of experience
- `maxResults`: Stop after N jobs (default: 50)

### Example Queries

- "Full stack developer" + "Pune" + 2-4 years experience
- "Data scientist" + "Bangalore" + 3-6 years experience
- "DevOps engineer" + Remote jobs

## 📈 Use Cases

- **Recruitment automation** — Auto-discover candidates and open positions
- **Salary benchmarking** — Analyze tech salary trends in India
- **Market intelligence** — Track which companies are hiring for what skills
- **Job alerts** — Monitor new postings matching your criteria
- **AI-powered job search** — Let Claude/ChatGPT find your next role

## 🏷️ Tags

`jobs`, `india`, `tech-jobs`, `recruitment`, `instahyre`, `software-engineer`, `ai-agents`, `mcp`, `claude`, `chatgpt`, `job-search`, `salary-data`

---

**Built for AI agents** • Works with Claude, ChatGPT & AI agents via Apify MCP • Maintained by [roshtarg](https://github.com/roshtarg-cpu)
