# -*- coding: utf-8 -*-
from scraper import get_top_fa_movies
from scraper import get_imdb_rating
import pandas as pd
import selen
import sys
import os

num_movies=300
if len(sys.argv) > 1:
    num_movies=int(sys.argv[1])

print("Loading Top Movies Page...")

# Configure Chrome Webdriver and load Filmaffnity.
fa_driver = selen.configure_chrome_driver('https://www.filmaffinity.com/es/')

# Get movies' url.
movies_urls = selen.get_fa_urls(fa_driver, num_movies)

# close the driver.
fa_driver.close()

# Create images folder if it does not exist
if not os.path.exists('../images'):
    os.makedirs('../images')

print("\nStarting web scraping of Top Movies from FilmAffinity: {} movies"
      "".format(num_movies))
movies_dict = get_top_fa_movies(movies_urls)

# Configure Chrome Webdriver and load IMDb.
imdb_driver = selen.configure_chrome_driver('https://www.imdb.com/')

# Configure the search field to search movies only.
imdb_driver.find_element_by_xpath('//label[@aria-label="All"]').click()
imdb_driver.find_element_by_xpath('//a[@aria-label="Titles"]').click()

# Iterate the dictionary to get the rating and votes of IMDb and add them to it.
for movie in movies_dict.values():
    search_movie = movie['título']
    search_year = movie['año']
    imdb_driver, imdb_url = selen.get_imdb_url(imdb_driver, search_movie, search_year)
    imdb_rating = imdb_votes = ''
    if imdb_url:
        print("\nScraping {} from IMDb".format(search_movie))
        imdb_rating, imdb_votes = get_imdb_rating(imdb_url)
    movie.update({'puntuación_imdb': imdb_rating, 'votos_imdb': imdb_votes})

# close the driver.
imdb_driver.close()

# Write CSV file with the dataframe generated
movies_df = pd.DataFrame.from_dict(movies_dict, orient="index")
movies_df.to_csv('../movies.csv', encoding='utf-8-sig')

print("\nDataset created")