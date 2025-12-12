# 24sata News Titles Analysis

This project collects news headlines from the Croatian news website 24sata.hr using Python and analyzes the most common words.

## Overview

- Language & Tools: Python, BeautifulSoup, Requests, CSV, Collections (Counter), Regular Expressions  
- Goal: Scrape up to 300 news headlines, clean and filter words, and identify the most frequent relevant keywords.  
- Output:  
  - `naslovi.csv` – CSV file with all scraped headlines  
  - Console output of the 20 most frequent words  

## How it works

1. The script fetches the sitemap of 24sata.hr and extracts news URLs.  
2. Headlines (`<h1>` tags) are scraped from each URL.  
3. Text is cleaned by removing punctuation, numbers, stopwords, and short words (less than 3 letters).  
4. The most frequent words are counted and displayed in the console.  

## Usage

1. Clone the repository.  
2. Install required packages using `pip install -r requirements.txt`.  
3. Run the script with `python scrape_titles.py`.  

## Notes

- The script captures headlines available at the time of execution. New articles will appear only when the script is run again.  
- The stopwords list is extensive to ensure only relevant words are counted.  
- This project is intended for educational and portfolio purposes.  

## License

MIT License
