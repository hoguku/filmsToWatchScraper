import requests
from bs4 import BeautifulSoup

import csv

paramGenre = input("Enter genre (~ Horror): ")
paramLanguage = input("Enter original language (~ Japanese): ")

filename = 'films.csv'
csvfile = open(filename,'w',newline = '')
filmsDataset = csv.writer(csvfile)

url = 'https://www.themoviedb.org/movie'

session = requests.Session()
response = session.get(url, headers={'User-Agent': 'Mozilla/5.0'})

webpage = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
webpageBS = BeautifulSoup(webpage.content, "html.parser")
webpageBS.prettify()

filmGenres = webpageBS.find('ul', {"id": "with_genres"})
filmGenres = filmGenres.find_all('li')

genreId = -1
for genre in filmGenres:
    if (paramGenre == genre.a.string):
        genreId = genre.attrs['data-value']

if genreId != -1:
    page = 0
    result = True
    while page < 50:
        page = page + 1
        url = 'https://www.themoviedb.org/movie?with_genres=' + genreId + '&page=' + str(page)
        webpage = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpageBS = BeautifulSoup(webpage.content, "html.parser")
        webpageBS.prettify()

        films = webpageBS.find('div', {"id": "page_" + str(page)})
        films = films.find_all('div', {"class": "wrapper"})
        for film in films:
            film = film.find('a', {"class": "image"})
            filmUrl = 'https://www.themoviedb.org' + film['href']
            filmPage = requests.get(filmUrl, headers={'User-Agent': 'Mozilla/5.0'})
            filmPageBS = BeautifulSoup(filmPage.content, "html.parser")
            
            profile = filmPageBS.find('li', {'class':'profile'})
            director = "NULL"
            if profile:
                director = profile.a.get_text()
            facts = filmPageBS.find('div', {'class':'facts'})
            
            genre = "NULL"
            genres = facts.find('span', {'class':'genres'})
            if genres:
                genre = genres.a.get_text()

            #runtime = facts.find('span', {'class':'runtime'}).get_text()
            rank = str(filmPageBS.find('div', {'class':'user_score_chart'})['data-percent'])
            
            filmsDataset.writerow([film['title']] + [genre] + [rank] + [director])
            print(film['title'] + ": " + genre + " " + rank + " " + director)
else:
    print("Couldn't get the film dataset with the specified gender.")

