
"""	
This project will take you through the process of
mashing up data from two different APIs to make
movie recommendations. The TasteDive API lets you provide a
movie (or bands, TV shows, etc.) as a query
input, and returns a set of related items. The
OMDB API lets you provide a movie title as
a query input and get back data about the
movie, including scores from various review sites (Rotten Tomatoes,
IMDB, etc.).
"""

#requests is a python HTTP library to send and recieve HTTP requests.
#it is most widely used python library for working with REST APIs

import requests
"""
It should take two input parameter, a string that
is the name of a movie or music artist
and the API key's. The function should return the
5 TasteDive results that are associated with that string;
rigth now it only get movies, not other kinds
of media. It will return a python dictionary with
just one key, ‘Similar’.
"""

def get_movies_from_tastedive(movieName, key="392852-MOHTARAH-C4DXJUM4"):
    baseurl="https://tastedive.com/api/similar"
    params_d = {}
    params_d["q"]= movieName
    params_d["k"]= key
    params_d["type"]= "movies"
    params_d["limit"] = "5"
    resp = requests.get(baseurl, params=params_d)
    print(resp.url)
    respDic = resp.json()
    return respDic 

"""
Extracts just the list of movie titles from a dictionary
"""

def extract_movie_titles(movieName):
    result=[]
    for listRes in movieName['Similar']['Results']:
        result.append(listRes['Name'])
    return result


"""
It takes a list of movie titles as input. It gets five related movies
for each from TasteDive, extracts the titles for all of them, and combines
them all into a single list. Don’t include the same movie twice.
"""

def get_related_titles(listMovieName):
    if listMovieName != []:
        auxList=[]
        relatedList=[]
        for movieName in listMovieName:
            auxList = extract_movie_titles(get_movies_from_tastedive(movieName))
            for movieNameAux in auxList:
                if movieNameAux not in relatedList:
                    relatedList.append(movieNameAux)
        
        return relatedList
    return listMovieName

"""
It takes in one parameter which is a string that should represent the title
of a movie you want to search. The function should return a dictionary with information
about that movie.
"""

def get_movie_data(movieName, key="e8a0f132"):
    baseurl= "http://www.omdbapi.com/"
    params_d = {}
    params_d["t"]= movieName
    params_d["apikey"]= key
    params_d["r"]= "json"
    resp = requests.get(baseurl, params=params_d)
    print(resp.url)
    respDic = resp.json()
    return respDic

"""
It takes an OMDB dictionary result for one movie and extracts the
Rotten Tomatoes rating as an integer.
If there is no Rotten Tomatoes rating, return 0.
"""
def get_movie_rating(movieNameJson):
    strRating=""
    #print(movieNameJson)
    try:
        for typeRatingList in movieNameJson["Ratings"]:
            if typeRatingList["Source"]== "Rotten Tomatoes":
                strRating = typeRatingList["Value"]
    except:
        return 0
    if strRating != "":
        rating = int(strRating[:-1])
    else: rating = 0
    return rating

def get_sorted_recommendations(listMovieTitle):
    listMovie= get_related_titles(listMovieTitle)
    lst_of_movie=[(i,get_movie_rating(get_movie_data(i))) for i in listMovie]
    final_list= sorted(lst_of_movie,key = lambda x:x[1], reverse=True)
    return final_list

lst_of_movies=input("Enter the name of movies on basis of which you would want recomendation:").split(",")
similar_movies=get_sorted_recommendations(lst_of_movies)

string="""movies similar to the entered list of movies and
sorted by rotten tomatoes ratings:"""

print(string)

for movie,rating in similar_movies:
    if rating!=0:
        print(movie,"has rating",rating)
    else:
        print(movie,"rating unavailable")
