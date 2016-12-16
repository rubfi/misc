import urllib2
import json
import lxml.html
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

def get_mean(act):

    act_enc = urllib2.quote(act.encode("utf-8"))

    response = urllib2.urlopen('http://www.imdb.com/xml/find?json=1&nr=1&nm=on&q='+act_enc)
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
                print "Processsing: "+ act +", Title: ",movie_data['Title']
                if movie_data['Year'].isdigit():
                    movie_values = [movie_id, movie_data['Title'], movie_data['Year'], movie_data['Released'], movie_data['Metascore'], movie_data['imdbRating'], movie_data['tomatoRating']]
                    movie_list.append(movie_values)

    df = pd.DataFrame(movie_list, columns=['id', 'Title', 'Year', 'Released', 'Metascore', 'imdbRating', 'tomatoRating'])
    df.set_index('id')
    df.imdbRating = pd.to_numeric(df.imdbRating, errors='coerce')
    df.tomatoRating = pd.to_numeric(df.tomatoRating, errors='coerce')
    df.Metascore = pd.to_numeric(df.Metascore, errors='coerce')

    mean = df.groupby('Year').agg({'imdbRating': [np.mean]})

    return mean


pa = get_mean ("Patricia Arquette")
ld = get_mean("Leonardo DiCaprio")
jc = get_mean("Jennifer Connelly")
nc = get_mean("Nicolas Cage")

plt.plot(pa.index,pa[[0]],label="Patricia Arquette")
plt.plot(ld.index,ld[[0]],label="Leonardo DiCaprio")
plt.plot(nc.index,nc[[0]],label="Nicolas Cage")
plt.plot(jc.index,jc[[0]],label="Jennifer Connelly")

fp = FontProperties()
fp.set_size('small')
plt.legend( loc='upper right', numpoints = 1, prop = fp)
plt.xticks(np.arange(1980, 2017, 1.0), rotation=45)
plt.title('Average IMDb rating per year')
plt.grid()
plt.show()

