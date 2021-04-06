# -*- coding: utf-8 -*-
from scraper import get_top_fa_movies
from scraper import get_imdb_rating
import pandas as pd
import os
import selen

print("Loading Top Movies Page...")

# Configure Chrome Webdriver and load Filmaffnity.
fa_driver = selen.configure_chrome_driver('https://www.filmaffinity.com/es/')

# Get movies' url.
movies_urls = selen.get_fa_urls(fa_driver, 300)

# close the driver.
fa_driver.close()

# Create images folder if it does not exist
if not os.path.exists('../images'):
    os.makedirs('../images')

print("Starting web scraping of Top Movies from FilmAffinity: {} movies"
      "".format(len(movies_urls)))
movies_dict = get_top_fa_movies(movies_urls)

# Configure Chrome Webdriver and load IMDb.
imdb_driver = selen.configure_chrome_driver('https://www.imdb.com/')

# Configure the search field to search movies only.
imdb_driver.find_element_by_xpath('//label[@aria-label="All"]').click()
imdb_driver.find_element_by_xpath('//a[@aria-label="Titles"]').click()

# Iterate the dictionary to get the rating and votes of IMDb and add them to it.
for k, v in movies_dict.items():
    search_movie = v['título']
    search_year = v['año']
    imdb_driver, imdb_url = selen.get_imdb_url(imdb_driver, search_movie, search_year)
    if(imdb_url == ''):
        imdb_rating = ''
        imdb_votes = ''
    else:
        print("\nScraping {} from IMDb".format(search_movie))
        imdb_rating, imdb_votes = get_imdb_rating(imdb_url)
    v.update({'imdb_rating': imdb_rating, 'imdb_votes': imdb_votes})

# close the driver.
imdb_driver.close()

movies_df = pd.DataFrame.from_dict(movies_dict, orient="index")
movies_df.to_csv('../movies.csv', encoding='utf-8-sig')

print("\nDataset created")