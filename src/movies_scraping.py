# -*- coding: utf-8 -*-
import pandas as pd
from scraper import get_top_fa_movies


movies_urls = ["https://www.filmaffinity.com/es/film809297.html",
               "https://www.filmaffinity.com/es/film730528.html",
               "https://www.filmaffinity.com/es/film236748.html"]

print("Starting web scraping of Top Movies from FilmAffinity: {} movies"
      "".format(len(movies_urls)))
movies_dict = get_top_fa_movies(movies_urls)
movies_df = pd.DataFrame.from_dict(movies_dict, orient="index")
movies_df.to_csv('../movies.csv', encoding='utf-8-sig')