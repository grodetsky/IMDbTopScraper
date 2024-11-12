import csv
import json
import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm


def convert_to_minutes(runtime_str):
    hours = int(re.search(r'(\d+)h', runtime_str).group(1)) * 60 if re.search(r'(\d+)h', runtime_str) else 0
    minutes = int(re.search(r'(\d+)m', runtime_str).group(1)) if re.search(r'(\d+)m', runtime_str) else 0
    return hours + minutes if (hours + minutes) > 0 else ""


def convert_to_millions(amount_str):
    cleaned_text = re.sub(r'[^\d.]', '', amount_str)
    return round(float(cleaned_text) / 1_000_000, 2)


with open("imdb_movie_links_for_scraping.json", "r", encoding="utf-8") as file:
    movie_links = json.load(file)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
}

with open("imdb_movie_data.csv", mode='w', newline='', encoding='utf-8-sig') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(
        ["Rank", "Title", "Year", "Country", "Genre", "Director", "Runtime (Minutes)", "Rating", "Metascore",
         "Budget (Millions)", "Revenue (Millions)"])

    for sample_movie in tqdm(movie_links, desc="Processing movies", unit="movie"):
        try:
            response = requests.get(sample_movie["Link"], headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract the release year
            release_year = soup.find('a', string=re.compile(r'^\d{4}$'))
            year_text = release_year.text.strip() if release_year else ""

            # Extract country of origin
            country_container = soup.find('li', {'data-testid': 'title-details-origin'})
            country_tag = country_container.find('a', {'class': 'ipc-metadata-list-item__list-content-item'})
            country_text = country_tag.text.strip() if country_tag else ""

            # Extract genres
            genre_container = soup.find('div', {'class': 'ipc-chip-list__scroller'})
            genre_text = ", ".join([genre.text for genre in genre_container.find_all('span', {
                'class': 'ipc-chip__text'})]) if genre_container else ""

            # Extract director(s)
            director_container = soup.find('li', {'data-testid': 'title-pc-principal-credit'})
            director_text = ", ".join(
                [director.text.strip() for director in
                 director_container.find_all('a')]) if director_container else ""

            # Extract runtime in minutes
            runtime_tag = soup.find('ul',
                                    class_='ipc-inline-list ipc-inline-list--show-dividers sc-ec65ba05-2 joVhBE baseAlt').find_all(
                'li', class_='ipc-inline-list__item')[-1].text.strip()
            runtime_value = convert_to_minutes(runtime_tag) if runtime_tag else ""

            # Extract the movie rating
            rating_tag = soup.find('span', {'class': 'sc-d541859f-1 imUuxf'})
            rating_value = float(rating_tag.text.strip()) if rating_tag else ""

            # Extract metascore
            metascore_tag = soup.find('span', {'class': 'metacritic-score-box'})
            metascore_value = int(metascore_tag.text.strip()) if metascore_tag else ""

            # Extract budget in millions
            budget_container = soup.find('li', {'data-testid': 'title-boxoffice-budget'})
            budget_tag = budget_container.find('span',
                                               class_='ipc-metadata-list-item__list-content-item') if budget_container else None
            budget_value = convert_to_millions(budget_tag.text.strip()) if budget_tag else ""

            # Extract revenue in millions
            revenue_container = soup.find('li', {'data-testid': 'title-boxoffice-cumulativeworldwidegross'})
            revenue_tag = revenue_container.find('span',
                                                 class_='ipc-metadata-list-item__list-content-item') if revenue_container else None
            revenue_value = convert_to_millions(revenue_tag.text.strip()) if revenue_tag else ""

            csv_writer.writerow(
                [sample_movie["Rank"], sample_movie["Title"], year_text, country_text, genre_text,
                 director_text, runtime_value, rating_value, metascore_value, budget_value, revenue_value])

        except Exception as e:
            print(f"Error extracting data for {sample_movie['Rank']}. {sample_movie['Title']}: {e}")

    print("Data extraction completed.")
