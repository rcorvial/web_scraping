# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import http_utils
import time
import re


def get_movie_info(html_content, movie_dict):
    """
    Fill the dictionary with the information of the movie obtained from the
    HTML.

    :param BeautifulSoup html_content: Object with the HTML content of the
                                       movie
    :param: dict film_dict: Dictionary to store the information of the movie
    """
    # Sections that want to be obtained
    filter_sections = ["Título original", "Duración", "Año", "País",
                       "Dirección", "Guion", "Reparto", "Productora",
                       "Género", "Sinopsis"]

    # Movie info is under the first tag <dl class="movie-info">
    movie_info = html_content.find("dl", {"class": "movie-info"})
    
    # Section names use the tag "dt" and section values use the tag "dd"
    sections = movie_info.find_all("dt")
    values = movie_info.find_all("dd")

    for section, value in zip(sections, values):
        if section.string in filter_sections:
            # Use a different way to obtain the information in section "Título
            # original" because in some cases it has a button "aka" that want
            # to be omitted.
            if section.string == "Título original":
                content = value.contents[0].strip()
            else:
                content = value.get_text().strip()

            # Remove all additional spaces that could appear between words
            content = " ".join(content.split())

            movie_dict[section.string.lower().replace(" ", "_")] = content


def get_movie_awards(html_content, movie_dict):
    """
    Fill the dictionary with the awards information of the movie obtained
    from the HTML.

    :param BeautifulSoup html_content: Object with the HTML content of the
                                       movie
    :param: dict film_dict: Dictionary to store the award information
    """
    # Movie awards are under the first tag <dd class="award">
    awards = html_content.find("dd", {"class": "award"})
    
    if awards:
        # Store awards as a list
        movie_dict['premios'] = []

        # Each award is under the tag <div class="margin-bottom">
        for award in awards.find_all("div", {"class": "margin-bottom"}):
            movie_dict['premios'].append(award.get_text().strip())


def get_rating(html_content, movie_dict):
    """
    Fill the dictionary with the rating of the movie obtained from the HTML.

    :param BeautifulSoup html_content: Object with the HTML content of the
                                       movie
    :param: dict film_dict: Dictionary to store the rating and votes
    """
    # Rating is under the first tag <div id="movie-rat-avg">
    rating = html_content.find(id="movie-rat-avg").get_text().strip()
    rating = rating.replace(",", ".")
    movie_dict['puntuación_fa'] = float(rating)

    # Votes is under the first tag <span itemprop="ratingCount">
    votes = html_content.find(itemprop="ratingCount").get_text().strip()
    votes = votes.replace(".", "")
    movie_dict['votos_fa'] = int(votes)


def get_professional_rating(html_content, movie_dict):
    """
    Fill the dictionary with the professional rating of the movie obtained
    from the HTML.

    :param BeautifulSoup html_content: Object with the HTML content of the
                                       movie
    :param: dict film_dict: Dictionary to store the professional rating
    """
    # Professional rating is under the first tag <div class="legend-wrapper">
    professional_rating = html_content.find("div", {"class": "legend-wrapper"})
    
    if professional_rating:
        # There are three types of ratings (positive, neutral and negative)
        # and each type is under the tag <div class="leg">
        prof_rating = professional_rating.find_all('div', {'class': 'leg'})
        movie_dict['puntuación_positiva'] = prof_rating[0].get_text().strip()
        movie_dict['puntuación_neutral'] = prof_rating[1].get_text().strip()
        movie_dict['puntuación_negativa'] = prof_rating[2].get_text().strip()


def get_poster(html_content, movie_dict):
    """
    Download the poster of the movie and store in the dictionary the URL to
    the image and the local path where the image is saved.

    :param BeautifulSoup html_content: Object with the HTML content of the
                                       movie
    :param: dict film_dict: Dictionary to store the poster information
    """
    # Set poster name and path to save it
    poster_name = movie_dict['título']+movie_dict['año'].replace(" ", "")
    # Name of the file should only have alphanumeric characters.
    jpg_name =  re.sub(r"[^a-zA-Z0-9]", "", poster_name)
    poster_path = "../images/{}.jpg".format(jpg_name)

    # Poster ULR is in the first tag <img itemprop="image"...src="URL">
    poster_url = html_content.find('img', {"itemprop": "image"})['src']

    if poster_url:
        # Get poster image from the URL
        print("Download poster of the movie in {}".format(poster_path))
        poster = http_utils.get_url_content(poster_url)
        
        # Save poster image in a JPG file in the folder "images"
        output = open(poster_path, "wb")
        for chunk in poster:
            output.write(chunk)
        output.close()
    
        movie_dict['portada_url'] = poster_url
        movie_dict['portada_local'] = poster_path


def get_top_fa_movies(urls_list):
    """
    Get a dictionary of dictionaries with the information of the movies
    obtained from the URLs received as parameter.

    :param list urls_list: URLs to the movies whose information want to be
                           obtained.
    :return: dict: Dictionary with the information of the movies
    """
    # Dictionary to store all the information obtained from the URLs
    movies_dict = dict()

    # Index to store the movies
    index = 0
    
    # Loop each URL to get movies information
    for url in urls_list:
        # Create an empty dictionary to store the information
        movies_dict[index] = dict()

        print("\nScraping movie {}".format(index))
        init_time = time.time()
        page = http_utils.get_url_content(url)
        
        # Get an HTTP response delay estimation to wait for the next HTTP
        # request
        reponse_delay = time.time() - init_time

        # Get the HTML content
        page_content = BeautifulSoup(page.content, "html.parser")

        # Get the information of the movie from the HTML
        movies_dict[index]['título'] = \
            page_content.find(id="main-title").get_text().strip()
        print("Movie title: {}".format(movies_dict[index]['título']))
        get_movie_info(page_content, movies_dict[index])
        get_movie_awards(page_content, movies_dict[index])
        get_rating(page_content, movies_dict[index])
        get_professional_rating(page_content, movies_dict[index])
        get_poster(page_content, movies_dict[index])

        # Next movie
        index += 1
        
        # Wait 5x HTTP response delay for the next HTTP request
        time.sleep(5*reponse_delay)
    
    return movies_dict
    

def get_imdb_rating(url_movie):
    """
    Get the rating and votes counter of a movie from IMDb
    :param str url_movie: URL to the movie whose rating want to be obtained.
    :return: (float, int): Rating of the movie and number of votes
    """
    # HTTP request
    page = http_utils.get_url_content(url_movie)
    
    # Get the HTML content
    page_content = BeautifulSoup(page.content, "html.parser")
    
    # Get rating value and number of votes
    rating = page_content.find('span', {'itemprop': 'ratingValue'}).get_text()
    rating = float(rating.strip().replace(",", "."))

    votes = page_content.find('span', {'itemprop': 'ratingCount'}).get_text()
    votes = int(votes.strip().replace(".", ""))

    return rating, votes