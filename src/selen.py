import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains


def configure_chrome_driver():
    """
    Configure Chrome Webdriver.

    :return: Webdriver: Chrome Webdriver.
    """
    # Add additional Options to the webdriver
    chrome_options = ChromeOptions()

    # add the argument and make the browser Headless.
    chrome_options.add_argument("--headless")

    # Instantiate the Webdriver
    driver = webdriver.Chrome(executable_path="./chromedriver.exe", options = chrome_options)
    return driver


def get_movies_urls(driver):
    """
    Navigate to the Top-FA page.
    Load the top 90 movies.
    Create a list with the urls of the movies.

    :param : Webdriver: Chrome Webdriver.
    :return: list movie_list: list with the urls of each movie.
    """
    # Open the webpage with the webdriver
    driver = webdriver.Chrome('./chromedriver.exe')
    driver.get('https://www.filmaffinity.com/es/')

    # Wait between 1 to 2 seconds
    sleep(random.uniform(1, 2))

    # Accept conditions
    driver.find_element_by_xpath("//button[contains(text(),'ACEPTO')]").click()

    # Wait between 1 to 2 seconds
    sleep(random.uniform(1, 2))

    # Go to the page with the top-movies
    driver.find_element_by_link_text("Top FA").click()

    # Wait between 1 to 2 seconds
    sleep(random.uniform(1, 2))

    # Exlcude TV-Shows
    driver.find_element_by_xpath("//label[contains(text(),'Series de TV')]").click()

    # Wait between 1 to 2 seconds
    sleep(random.uniform(1, 2))

    # Apply the filter
    driver.find_element_by_xpath('//input[@value="Aplicar Filtro"]').click()

    # Wait betweens 1 to 2 seconds
    sleep(random.uniform(1, 2))

    #  loop to show 90 movies
    for i in range(2):
        # Scroll to the end of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Find the element to show more movies
        more_movies = driver.find_element_by_xpath('//div[@title="Ver más resultados"]')

        # Wait between 1 to 2 seconds
        sleep(random.uniform(1, 2))

        # Move the mouse pointer over the element.
        ActionChains(driver).move_to_element(more_movies).perform()

        # Wait between 1 to 2 seconds
        sleep(random.uniform(1, 2))

        # After scrolling and place the mouse over the element,
        # it is possible to show 30 extra movies by clicking on it.
        driver.find_element_by_xpath('//div[@title="Ver más resultados"]').click()

        # Wait between 1 to 2 seconds
        sleep(random.uniform(1, 2))

    # Get the element withe all the movies
    top_movies_element = driver.find_element_by_id('top-movies')

    # Get all the elements with the content of each movie
    content_list = top_movies_element.find_elements_by_class_name('content')

    # Empty list to store the urls of the movies
    movie_list = []

    for content in content_list:

        # Append each url to the list
        movie_list.append(content.find_element_by_class_name('mc-title').find_element_by_tag_name('a').get_attribute('href'))

    return movie_list