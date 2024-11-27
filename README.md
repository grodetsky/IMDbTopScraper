# IMDb Movie Scraper

This project automates the process of extracting movie information from IMDb's Top 1000 movies list. It consists of two main parts: extracting movie links and scraping detailed movie information. The results are saved as JSON and CSV files for further analysis.

## Features

- Extracts movie links from IMDb's Top 1000 movies list.
- Scrapes detailed movie data, including:
  - Rank
  - Title
  - Release Year
  - Country
  - Genre
  - Director
  - Runtime (in minutes)
  - IMDb Rating
  - Metascore
  - Budget (in millions)
  - Worldwide Revenue (in millions)
- Saves movie links as JSON and movie details as CSV.

---
## How to Use

1. **Set Up Environment**
   - Clone the repository.
   - Install the required Python dependencies using `pip install -r requirements.txt`.

2. **Run the Main Script**
   Execute the `main.py` script to run the full scraping pipeline:
   ```bash
   python main.py
   ```
   
3. **Check Output**
   - **Movie Links**: Saved in `data/imdb_movie_links_for_scraping.json`.
   - **Movie Details**: Saved in `data/imdb_movie_data.csv`.

---

## Notes

- If the scraper stops working, inspect IMDb's website for updates to element selectors.
- Ensure the correct browser driver version is installed.