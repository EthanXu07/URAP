
import csv
from os import name
import requests
from bs4 import BeautifulSoup
import time


url = 'https://www.aeaweb.org/journals/aer/issues'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
data = []

def validtime(href):
    vurl = "https://www.aeaweb.org/" + href
    vresponse = requests.get(vurl)
    vsoup = BeautifulSoup(vresponse.text, "html.parser")  
    issue_info =vsoup.find(string=lambda text: text and "Vol." in text)
    info = issue_info.strip()
    parts = info.split(' ')
    date = int(parts[len(parts)-1])
    #print(date)
    if date ==2025 or date == 2024:
        return True
    else:
        return False

def findvalidissues(links):
    useablelinks = []
    for link in links:
        href = link.get('href')
        if href.startswith('/issues'):
            #print(href)  
            if validtime(href):
                useablelinks.append(href)
            elif len(useablelinks) > 0:
                break
    return useablelinks

def finddate(soup):
    issue_info =soup.find(string=lambda text: text and "Vol." in text)
    info = issue_info.strip()
    parts = info.split(' ')
    date = parts[len(parts)-2] + " " + parts[len(parts)-1]
    return date

def find_num_references_crossref(doi):
    url = f"https://api.crossref.org/works/{doi}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print('success')
        return data["message"].get("is-referenced-by-count", 0)  # times cited
    else:
        print(f"Error {response.status_code} for DOI {doi}")
        return None

if __name__ == "__main__":
    links = soup.find_all('a',href = True)
    useablelinks = findvalidissues(links)


    for link in useablelinks:
        url = "https://www.aeaweb.org/" + link
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.select("article.journal-article")
        currdate = finddate(soup)

        for art in articles:
            title_tag = art.select_one("h3.title a")
            if not title_tag:
                continue

            title = title_tag.get_text(strip=True)

            # Skip "Front Matter", "Back Matter", and section dividers
            if title.lower() in ("front matter", "back matter"):
                continue

            author_div = art.select_one(".article-item-authors .author")
            if not author_div:
                continue  

            authors = author_div.get_text(" ", strip=True)
            authors = authors.replace("by", "", 1).strip()

            doi = art.get("id")  # DOI "10.1257/aer.20231468"
            num_references = find_num_references_crossref(doi) if doi else None
            time.sleep(1) 
            data.append({"title": title, "authors": authors, "date": currdate, "num_references": num_references})
 
    with open("articles.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "authors", "date", "num_references"])
        writer.writeheader()
        writer.writerows(data)
    
    print(f"Wrote {len(data)} articles to articles.csv")


    