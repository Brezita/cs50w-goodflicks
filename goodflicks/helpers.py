''' Manages API helper functions. '''

import urllib.request
import json

from .utils import TMDB_API_KEY, STREAMING_HEADERS

# Any functions that call 

# Function to fetch TMDb Config Data from API
# This is gonna require code from the old index function
def config():
    # If there is already a file write to that
    # If not, create a new one
    return 0

# Function to fetch config data from file given a list of parameters
def fetch_config():
    return 0

# Return a list of all countries supported by Streaming Availability
def countries():
    data = jsdecode(urllib.request.urlopen(urllib.request.Request("https://streaming-availability.p.rapidapi.com/countries", headers=STREAMING_HEADERS)))
    
    with open("goodflicks/static/goodflicks/countries.json", "w") as countryfile:
        json.dump(data, countryfile)

    countryfile.close()
    return 0

# Return a list of all genres from SA and TMDB
def genres():
    # Make requests to get genre data
    sadata = jsdecode(urllib.request.urlopen(urllib.request.Request("https://streaming-availability.p.rapidapi.com/genres", headers=STREAMING_HEADERS)))
    moviedata = jsdecode(urllib.request.urlopen("https://api.themoviedb.org/3/genre/movie/list?api_key=0e362400ddffa49641d21e285ad6b8dd"))
    tvdata = jsdecode(urllib.request.urlopen("https://api.themoviedb.org/3/genre/tv/list?api_key=0e362400ddffa49641d21e285ad6b8dd"))

    for value in range(len(moviedata['genres'])):
        sadata.update({moviedata['genres'][value]['id']: moviedata['genres'][value]['name']})
    
    for value in range(len(tvdata['genres'])):
        sadata.update({tvdata['genres'][value]['id']: tvdata['genres'][value]['name']})

    data = dict(sorted(sadata.items(),key= lambda x:x[1]))

    # Save to a file
    with open("goodflicks/static/goodflicks/genres.json", "w") as genrefile:
        json.dump(data, genrefile)

    genrefile.close()
    return 0

    # Need to work out a way of tackling the genres that don't overlap
    # When the server starts, check in file when this was last run
    # If it was last run over a week ago/never run, fetch from API
    return 0

# Fetch the countries file or the genres file depending
# Then turn json into Python dictionary
def fetch(filename):
    f = open("goodflicks/static/goodflicks/" + filename + ".json", "r")
    content = f.read()
    content = json.loads(content)
    return content

# CONSIDER MERGING THE FOLLOWING TWO FUNCTIONS:
# Function to grab an image URL, given a specific TMDb IDd
# CHANGE TO: given a dataset, will extract the image URL and ID and zip them together
# Also needs to be rewritten to account for "media_type": "tv" as this is currently throwing exceptions
def imgdata(dataset):
    imgurls = []
    tmdb_id = []

    for item in dataset:
        if "tmdbID" in item:
            imgurls.append(item['posterPath'])
            tmdb_id.append(item["tmdbID"])
        else:
            if item["media_type"] == "tv" or item["media_type"] == "movie":  
                imgurls.append(item['poster_path'])
                tmdb_id.append(item["id"])

    imagedata = zip(imgurls, tmdb_id)
    return imagedata

# Given the result of a particular request, will decode the JSON data
def jsdecode(result):
    #config_result = urllib.request.urlopen(config_url)
    data = result.read().decode()
    jsdata = json.loads(data)
    return jsdata

# Given a list of countrycodes, will call an API and decode them
def decodecountry(countries):
    countrystring = ";".join(countries)
    data = jsdecode(urllib.request.urlopen(f"https://restcountries.eu/rest/v2/alpha?codes={countrystring}"))
    countlist = {}
    for item in data:
        countlist.update({item['alpha2Code']: item['name']})
    return countlist

''' The below code is the former index page function. I might use bits of this code somewhere else so I'm preserving it for posterity. '''
        # # Make a call to the Availability API for each of the user's favourite genres for all services available for TV and movies
        # # (Currently making a test call for just one)

        # services = list(request.user.services.split(","))
        # genrelist = list(request.user.genres.split(","))
        # country = "gb"
        # mediatype = "movie" 

        # # Need to rewrite this to abstract away
        # # Call the API for each service to abstract 
        # data = {}
        # for item in services: 
        #     print(item)
        #     # This is throwing errors if the genre code isn't valid on streaming availability
        #     # Genres probably needs to be reworked to only contain SA genres -
        #     # not sure genres are actually used elsewhere at all? (Maybe in search)

        #     url = f"https://streaming-availability.p.rapidapi.com/search/basic?country={country}&service={item}&type={mediatype}&genre={random.choice(genrelist)}"
        #     print(url)

        #     req = urllib.request.Request(url, headers=STREAMING_HEADERS)
        #     result = jsdecode(urllib.request.urlopen(req))
        #     data[item] = imgdata(result['results'])

        # # Rewrite to grab config data from config file
        # config_url = f"https://api.themoviedb.org/3/configuration?api_key={TMDB_API_KEY}"
        # config_result = urllib.request.urlopen(config_url)
        # config_data = config_result.read().decode()
        # config_jsdata = json.loads(config_data)
        
        # for service in data:
        #     print(data[service])
        
        # # Don't forget to rewrite this so the template gets the number of pages too!
        # return render(request, 'goodflicks/index.html', {
        #     "data": data,
        #     "imgurl": config_jsdata["images"]["base_url"],
        #     "imgsize": config_jsdata["images"]["poster_sizes"][1]
        # })        
