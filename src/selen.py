import random
import math
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def configure_chrome_driver(webpage):
    """
    Configure Chrome Webdriver and load a webpage.

    :return: Webdriver: Chrome Webdriver.
    """
    # Add additional Options to the webdriver
    chrome_options = ChromeOptions()

    # Make the browser Headless.
    chrome_options.add_argument("--headless")
    # Configure windows size to avoid problem by finding items.
    chrome_options.add_argument("--window-size=1920,1080")

    # Instantiate the Webdriver
    driver = webdriver.Chrome(executable_path="./chromedriver.exe", options = chrome_options)

    # Open the webpage with the webdriver
    driver.get(webpage)

    return driver


def get_fa_urls(fa_driver, movie_number):
    """
    Navigate to the Top-FA page.
    Load the top 90 movies.
    Create a list with the urls of the movies.

    :param : Webdriver fa_driver: Chrome Webdriver with Filmaffinity loaded.
    :param : Webdriver int: number of movies to list.

    :return: list movie_list: list with the urls of each movie.
    """

    # Explicit Wait. Wait maximum of 10 seconds for some actions.
    wait = WebDriverWait(fa_driver, 10)

    # Accept conditions
    wait.until(EC
    .element_to_be_clickable((By.XPATH,"//button[contains(text(),'ACEPTO')]"))).click()

    # Go to the page with the top-movies
    wait.until(EC
    .element_to_be_clickable((By.LINK_TEXT,"Top FA"))).click()

    # Exlcude TV-Shows
    wait.until(EC
    .element_to_be_clickable((By.XPATH,"//label[contains(text(),'Series de TV')]"))).click()

    # Apply the filter
    wait.until(EC
    .element_to_be_clickable((By.XPATH,'//input[@value="Aplicar Filtro"]'))).click()

    # Number of iteration to get more movies.
    loop_range = math.floor(movie_number/30)
    
    # loop to show more than 30 movies
    for i in range(loop_range):
        # Scroll to the end of the page
        fa_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait between 1 to 2 seconds
        sleep(random.uniform(1, 2))
        
        # Find the element to show more movies
        more_movies = wait.until(EC.visibility_of_element_located((By.ID,'load-more-bt')))

        # Move the mouse pointer over the element.
        ActionChains(fa_driver).move_to_element(more_movies).perform()

        # Wait between 1 to 2 seconds
        sleep(random.uniform(1, 2))

        # After scrolling and place the mouse over the element,
        # it is possible to show 30 extra movies by clicking on it.
        wait.until(EC.element_to_be_clickable((By.ID,'load-more-bt'))).click()
        
        # Wait between 1 to 2 seconds
        sleep(random.uniform(1, 2))

    # Get the element withe all the movies
    top_movies_element = fa_driver.find_element_by_id('top-movies')

    # Get all the elements with the content of each movie
    content_list = top_movies_element.find_elements_by_class_name('content')

    # Empty list to store the urls of the movies
    movie_list = []

    for content in content_list:
        # Append each url to the list
        movie_list.append(content.find_element_by_class_name('mc-title')
        .find_element_by_tag_name('a').get_attribute('href'))

    movie_list = movie_list[:movie_number]
    return movie_list


def get_imdb_url(imdb_driver, movie, year):
    """
    Search a movie in IMDb and get the link of the movie.

    :param : Webdriver imdb_driver: Chrome Webdriver with IMDb loaded.
    :param : string movie: name of the movie.
    :param : strig year: year of the movie.

    :return: (Webdriver, string) driver, url: Webdriver and url of the movie.
    """

    search_field = imdb_driver.find_element_by_xpath('//input[@placeholder="Search IMDb"]')

    # Clear the search field and enter the movie name.
    search_field.clear()
    search_field.send_keys(movie)
    search_field.send_keys(Keys.RETURN)
    
    if(imdb_driver.find_elements_by_class_name('findSection') == []):
        return(imdb_driver, '')
    
    # Get the list of results
    MoviesSection = imdb_driver.find_element_by_class_name('findSection')
    results = MoviesSection.find_element_by_class_name('findList').find_elements_by_class_name('result_text')

    movie_year = movie + ' (' + year + ')'

    url = ''

    # Iterate the result list.
    for i in range(3):
        for result in results:
            # Look if any element of the list match the name and year.
            if(result.text == movie_year and i == 0):
                url = result.find_element_by_tag_name('a').get_attribute('href')
                break

            # Look if any element of the list match the year.
            if(result.text[len(result.text)-5:len(result.text)-1] == year and i == 1):
                url = result.find_element_by_tag_name('a').get_attribute('href')
                break

            # Look if any element of the list match 'aka' name.
            if(result.text[result.text.find('aka ')+4:].replace('"','') == movie and i == 2):
                url = result.find_element_by_tag_name('a').get_attribute('href')
                break
            
        if(url != ''):
            break

    return(imdb_driver, url)
