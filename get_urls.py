import requests
from bs4 import BeautifulSoup

# URL sitemapa
sitemap_url = 'https://www.24sata.hr/news-sitemap.xml'

# Dohvat XML-a
response = requests.get(sitemap_url)
if response.status_code == 200:
    xml_content = response.text
    print("Sitemap dohvaćen!")
else:
    print("Greška pri dohvaćanju sitemap-a:", response.status_code)

# Parsanje XML-a
soup = BeautifulSoup(xml_content, 'xml')
urls = [loc.get_text() for loc in soup.find_all('loc')]

print(f"Pronađeno {len(urls)} URL-ova vijesti.")
print("Prvih 10 URL-ova:")
for u in urls[:10]:
    print(u)
