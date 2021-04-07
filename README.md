# Práctica 1: Web scraping

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4670450.svg)](https://doi.org/10.5281/zenodo.4670450)

## Descripción

Esta práctica está siendo realizada bajo el contexto de la asignatura _Tipología y ciclo de vida de los datos_, perteneciente al Máster en Ciencia de Datos de la Universitat Oberta de Catalunya. En ella, se aplican técnicas de _web scraping_ mediante el lenguaje de programación Python para extraer datos de las páginas web _Filmaffinty_ e _IMDb_. Con el objetivo de recompilar información sobre películas y comparar las puntuaciones dadas en cada una de las páginas, se genera un dataset en formato csv.

## Miembros del equipo

La actividad se realiza de manera conjunta por **Rafael Corvillo Alonso** y **Pablo López Ladrón de Guevara**.

## Ficheros del código fuente

* **src/movies_scraping.py**: punto de entrada al programa. Inicia el proceso de scraping y finaliza creando el dataset objetivo.
* **src/http_utils.py**: configuración para realizar las peticiones HTTP modificando la cabacera y capturando excepciones.
* **src/scraper.py**: contiene las funciones necesarias para scrapear las páginas de cada película en Filmaffinity. Esta información se almacenará en un diccionario. También se almacenan las imágenes en formato JPG correspondientes a las portadas de cada película. 
* **src/selen.py**: contiene las funciones necesarias para navegar por la web de Filmaffinity de manera dinámica y usar el buscador de películas de IMDb con ayuda de Selenium.

## Ejecución del proyecto

Para la ejecución del programa es necesario instalar las dependencias indicadas en el fichero _requirements.txt_, como se muestra a continuación:

```
pip install -r requirements.txt
```

El programa se ejecuta mediante el script _src/movies_scraping.py_ y tiene un parámetro opcional para indicar el número de películas que se quiere recopilar. Si no se indica un número, el valor por defecto son 300 películas. A continuación se muestra la ejecución del programa para recopilar información de las 500 películas con mejor puntuación de Filmaffinity:

```
python movies_scraping.py 500
```
