import requests
from bs4 import BeautifulSoup

# scrape abebooks for isbns
def get_isbns():
    all_links = []
    r = requests.get("https://www.abebooks.com/books/Textbooks/top-isbn.shtml")
    h = r.text
    soup = BeautifulSoup(h, 'html.parser')
    for link in soup.find_all('a'):
        mylink = link.get('href')
        if mylink != None and "/servlet/SearchResults?" in mylink:
            all_links.append(mylink[-10:])
    print(all_links)
    all_links = set(all_links)
    all_links = [x for x in all_links]
    return all_links