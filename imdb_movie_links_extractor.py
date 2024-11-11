import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

driver = webdriver.Chrome()
driver.get('https://www.imdb.com/search/title/?groups=top_1000&count=100&sort=user_rating,desc')

try:
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        try:
            driver.find_element(By.XPATH, '//span[text()="100 more"]').click()
            time.sleep(3)
        except:
            break

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    movies = [
        {
            "Rank": movie.a.get_text(strip=True).split('.', 1)[0],
            "Title": movie.a.get_text(strip=True).split('.', 1)[1].strip(),
            "Link": f"https://www.imdb.com{movie.a['href']}"
        }
        for movie in soup.select('div.sc-5bc66c50-0.bZBaVw')
    ]

    with open("imdb_movie_links_for_scraping.json", "w", encoding="utf-8") as file:
        json.dump(movies, file, ensure_ascii=False, indent=4)
finally:
    driver.quit()
    print("Movie titles and links saved to imdb_movie_links_for_scraping.json")
