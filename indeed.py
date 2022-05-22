import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?q=python&limit={LIMIT}"

def get_last_page():

    result = requests.get(URL)

    soup = BeautifulSoup(result.text, "html.parser")

    pagination = soup.find("div", {"class": "pagination"})
    links = pagination.find_all('a')
    pages = []

    for link in links[:-1]:
        pages.append(int(link.string))
        max_page = pages[-1]

        return max_page

def extract_job(html):
    title = html.find("h2", {"class": "jobTitle"}).find("span", title=True).string
    company = html.find("span", {"class": "companyName"}).string.strip()
    location = html.select_one("div.companyLocation").text
    job_id = html.find("h2",{"class":"jobTitle"}).find("a").get("data-jk")

    return {
        'title':title,
        'company':company,
        'location':location,
        'link': f"https://kr.indeed.com/viewjob?jk={job_id}"
    }

def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping Indeed: page {page}")
        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("td",{"class": "resultContent"})

        for result in results:
            job = extract_job(result)
            jobs.append(job)

    return jobs

def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs


