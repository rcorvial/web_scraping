# -*- coding: utf-8 -*-
from scraper import get_top_fa_movies
import pandas as pd
import os
import selen

print("Loading Top Movies Page...")
# Configure Chrome Webdriver.
driver = selen.configure_chrome_driver()

# Get movies' url.
movies_urls = selen.get_movies_urls(driver)

# close the driver.
driver.close()

# Create images folder if it does not exist
if not os.path.exists('../images'):
    os.makedirs('../images')

print("Starting web scraping of Top Movies from FilmAffinity: {} movies"
      "".format(len(movies_urls)))
movies_dict = get_top_fa_movies(movies_urls)

movies_df = pd.DataFrame.from_dict(movies_dict, orient="index")
movies_df.to_csv('../movies.csv', encoding='utf-8-sig')