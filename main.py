import os
from imdb_movie_links_extractor import extract_movie_links
from imdb_movie_info_scraper import scrape_movie_info

# Configuration
DATA_FOLDER = "data"
IMDB_TOP_URL = "https://www.imdb.com/search/title/?groups=top_1000&count=100&sort=user_rating,desc"
LINKS_FILE = os.path.join(DATA_FOLDER, "imdb_movie_links_for_scraping.json")
DATA_FILE = os.path.join(DATA_FOLDER, "imdb_movie_data.csv")


def main():
    # Ensure the data folder exists
    os.makedirs(DATA_FOLDER, exist_ok=True)

    # Step 1: Extract movie links
    print("Extracting movie links...")
    extract_movie_links(IMDB_TOP_URL, LINKS_FILE)
    print(f"Movie links saved to {LINKS_FILE}")

    # Step 2: Scrape movie details
    print("Scraping movie details...")
    scrape_movie_info(LINKS_FILE, DATA_FILE)
    print(f"Movie data saved to {DATA_FILE}")


if __name__ == "__main__":
    main()
