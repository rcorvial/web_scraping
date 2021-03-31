# Entrega parcial de la práctica 1: Web scraping

## Descripción

Esta práctica está siendo realizada bajo el contexto de la asignatura _Tipología y ciclo de vida de los datos_, perteneciente al Máster en Ciencia de Datos de la Universitat Oberta de Catalunya. En ella, se aplican técnicas de _web scraping_ mediante el lenguaje de programación Python para extraer datos de las páginas web _filmaffinty_ e _imdb_. Con el objetivo de recompilar información sobre películas y comparar las puntuaciones dandas en cada una de las páginas, se genera un dataset en formato csv.

## Miembros del equipo

La actividad se realiza de manera conjunta por **Rafael Corvillo Alonso** y **Pablo López Ladrón de Guevara**.

## Ficheros del código fuente

* **src/movies_scraping.py**: punto de entrada al programa. Inicia el proceso de scraping y finaliza creando el dataset objetivo.
* **src/http_utils.py**: configuración para realizar las peticiones HTTP modificando la cabacera y capturando excepciones.
* **src/scraper.py**: contiene las funciones necesarias para scrapear las páginas de cada película en Filmaffinity. Esta información se almacenará en un diccionario. También se almacenan las imágenes .jpg correspondientes a las portadas de cada película. 
* **src/selen.py**: contiene las funciones necesarias para navegar por la web de Filmaffinity de manera dinámica con ayuda de Selenium.

## Progreso actual

Para esta primera entrega parcial hemos implementado el código referente al scraper de las 90 películas mejor puntadas en la página _filmaffinity_. Mediante el uso de Selenium se navega desde la página principal hasta mostrar el top de películas deseadas. Las URLs de dichas películas se alamacenarán en una lista. Y a partir de esta lista se realizará con ayuda de BeautifulSoup webscraping en la página corerspondiente a cada película. Se recopilarán, entre otros, campos como el título, año, duración, país, premios, valoración, número de votos o crítica de profesionales. Todos los campos serán almacenados provisionalmente en un diccionario de diccionarios, para después generar un dataframe y finalmente el archivo _movies.csv_ objetivo. Además se obtendrán las imágenes correspondientes a las portadas de cada película y se almacenarán con formato jpeg en una carpeta llamada _images_.

## Puntos pendientes

* Dar respuesta a los diferentes puntos del informe.
* Completar el código del scraper:
    * Obtener las valoraciones y el número votos de cada película desde _imdb_. La idea es utilizar el campo de búsqueda de imdb para obtener la URL de cada película almacenda en el diccionario y así poder scrapear la información deseada. Dicha información se añadirá al conjunto de datos final.
    * Parametrizar la función principal, de forma que se pueda elegir el número de películas a almacenar en el archivo csv. Actualmente se almacenan 90 películas.

## Ejecución del proyecto

1. Abrimos la consola.
2. Nos situamos en la carpeta correspondiente al proyecto.
3. Creamos un entorno virtual y lo activamos.
4. Instalamos las librerías necesarias del archivo requirements.txt.
5. Ejecutamos el archivo movies_scraping.py.
