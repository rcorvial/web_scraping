# -*- coding: utf-8 -*-
from scraper import get_top_fa_movies
import pandas as pd
import os


movies_urls = ["https://www.filmaffinity.com/es/film809297.html",
               "https://www.filmaffinity.com/es/film730528.html",
               "https://www.filmaffinity.com/es/film236748.html"]

# Create images folder if it does not exist
if not os.path.exists('../images'):
    os.makedirs('../images')

print("Starting web scraping of Top Movies from FilmAffinity: {} movies"
      "".format(len(movies_urls)))
movies_dict = get_top_fa_movies(movies_urls)
movies_df = pd.DataFrame.from_dict(movies_dict, orient="index")
movies_df.to_csv('../movies.csv', encoding='utf-8-sig')