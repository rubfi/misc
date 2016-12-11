import urllib2
import json
import lxml.html
import pandas as pd
import numpy as np

act = "Angelina Jolie"

act = urllib2.quote(act.encode("utf-8"))

response = urllib2.urlopen('http://www.imdb.com/xml/find?json=1&nr=1&nm=on&q='+act)
data = json.load(response)

try:
    act_id = data['name_exact'][0]['id']
except:
    act_id = data['name_popular'][0]['id']

url = urllib2.urlopen('http://www.imdb.com/name/%s/'%(act_id))
html = url.read()
tree = lxml.html.fromstring(html)
elements = tree.find_class("filmo-row")
movie_list = []
for element in elements:
    [movie_role, movie_id] = element.get('id').split("-")
    if (movie_role == "actor") or (movie_role == "actress"):
        movie_url = urllib2.urlopen("http://www.omdbapi.com/?i=%s&tomatoes=true"%(movie_id))
        movie_data = json.load(movie_url)
        if movie_data['Response'] == "True": 
            print "Title: ",movie_data['Title']
            print "Rating: ",movie_data['imdbRating']
            movie_values = [movie_id, movie_data['Title'], movie_data['Year'], movie_data['Released'], movie_data['Metascore'], movie_data['imdbRating'], movie_data['tomatoRating']] 
            movie_list.append(movie_values)

df = pd.DataFrame(movie_list, columns=['id', 'Title', 'Year', 'Released', 'Metascore', 'imdbRating', 'tomatoRating'])
df.set_index('id')
df.imdbRating = pd.to_numeric(df.imdbRating, errors='coerce')
print df.imdbRating.describe()
print df[['Title', 'Year','imdbRating']].sort_values("imdbRating",ascending=0).head()
print df[['Title', 'Year','imdbRating']].sort_values("imdbRating",ascending=1).head()

