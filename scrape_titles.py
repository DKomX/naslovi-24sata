import requests
from bs4 import BeautifulSoup
import csv
from collections import Counter
import re

# --- STOP RIJEČI (proširena lista hrvatskih nebitnih riječi) ---
stop_rijeci = {
    "i", "u", "na", "je", "za", "se", "od", "a", "da",
    "koji", "koja", "koje", "su", "ga", "po", "o", "s",
    "do", "uz", "kao", "kod", "ili", "ali", "jer", "te",
    "što", "nije", "bi", "će", "prije", "poslije", "bez",
    "nakon", "sto",
    # dodano od korisnika
    "evo", "kako", "to", "je", "smo", "su", "ste",
    "sad", "sve", "isl",
    # dodatno ukloniti
    "ova", "ovo", "ovaj", "tako", "biti", "može",
    "među", "tijekom", "dok", "već", "protiv",
    "još", "samo", "tj", "preko", "nisu",
    "foto", "video", "pogledajte", "pogledaj", "pogledali",
    "bio", "pa", "mi", "dinama", "dinamo", "kaže", "rekli", 
    "rekla", "ovdje", "ima", "donosimo", "doznajemo",
    "otkriva", "otkrili", "otkrio", "hrvatska", "hrvatske",
    "hrvatskoj", "priča", "priče", "pričaju", "novo", "novi", "nova",
    "nove", "tko", "što", "gdje", "kada", "kako", "bivši", "bivša", 
    "bivše", "oni", "one", "ono", "njega", "nje", "njemu", "put", "puta",
    "sada", "vrlo", "više", "manje"
}

# --- 1. DOHVAT SITEMAPA ---
sitemap_url = 'https://www.24sata.hr/news-sitemap.xml'
response = requests.get(sitemap_url)

if response.status_code != 200:
    print("Greška pri dohvaćanju sitemap-a:", response.status_code)
    exit()

soup = BeautifulSoup(response.text, 'xml')
urls = [loc.get_text() for loc in soup.find_all('loc')]

print(f"Pronađeno {len(urls)} URL-ova vijesti.\n")

# --- 2. DOHVAT NASLOVA (300 najnovijih) ---
headers = {
    'User-Agent': 'PortfolioBot/1.0 (https://github.com/TvojeIme)'
}

naslovi = []

print("Dohvaćam 300 naslova...\n")

for url in urls[:300]:
    try:
        r = requests.get(url, headers=headers, timeout=6)
        if r.status_code != 200:
            continue

        soup = BeautifulSoup(r.text, 'html.parser')
        naslov = soup.find('h1')

        if naslov:
            naslov_clean = naslov.get_text(strip=True)
            naslovi.append(naslov_clean)
            print(naslov_clean)
    except:
        continue

print(f"\nUkupno dohvaćenih naslova: {len(naslovi)}")

# --- 3. SPREMANJE CSV ---
with open("naslovi.csv", 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["Naslov"])
    for n in naslovi:
        writer.writerow([n])

print("\nNaslovi spremljeni u 'naslovi.csv'")

# --- 4. OBRADA TEKSTA ---
svi = " ".join(naslovi).lower()
svi = re.sub(r'[^\w\s]', '', svi)
rijeci = svi.split()

# --- 5. FILTERI ---
# 5.1 stop riječi
rijeci = [r for r in rijeci if r not in stop_rijeci]
# 5.2 riječi kraće od 3 slova
rijeci = [r for r in rijeci if len(r) > 2]
# 5.3 riječi koje su samo brojevi
rijeci = [r for r in rijeci if not r.isdigit()]

# --- 6. BROJANJE NAJČEŠĆIH RIJEČI ---
brojac = Counter(rijeci)
najcesce = brojac.most_common(20)

print("\n20 najčešćih relevantnih riječi u naslovima:")
for r, b in najcesce:
    print(r, "-", b)
