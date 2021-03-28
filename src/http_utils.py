# -*- coding: utf-8 -*-
import requests


http_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,\
        image/avif,image/webp,image/apng,*/*;q=0.8,\
            application/signed-exchange;v=b3;q=0.9",
    "Accept-Enconding": "gzip, deflate, br",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "dnt": "1",
    "Pragma": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 \
            Safari/537.36"
}


def get_url_content(url):
    """
    Make a HTTP request to the URL and return the HTTP response with the
    information of the movie.

    :param str url: URL to the information of the movie
    :return: Reponse: Dictionary to store the information of the movie
    """
    try:
        print("HTTP request to the URL {}".format(url))
        page = requests.get(url, headers=http_headers, timeout=10)
    except requests.exceptions.Timeout:
        print("Timeout exceeded for URL {}".format(url))
    except requests.exceptions.RequestException:
        print("Broken connection for URL {}".format(url))
    finally:
        return page