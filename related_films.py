import requests_with_catching


# API keys
TASTEDIVE_KEY = '329737-RelatedF-U107S7OT'
OMDBAPI_KEY = 'fdfb7963'

def get_movies_from_tastedive(movie_title, k=TASTEDIVE_KEY, type='movies', limit_recommended=20):
    """Takes a movie title as an input and returns a TasteDive dictionary object
    containing movies related to the one passed as an argument.
    """
    base_url = 'https://tastedive.com/api/similar'
    dict_params = {}
    # parameter k: API key
    dict_params['k'] = k
    # parameter q: the search query
    dict_params['q'] = movie_title
    # parameter type: the type of the search query. Default 'movies'
    dict_params['type'] = type
    # parameter limit: maximum number of recommendations to retrieve. Default 20
    dict_params['limit'] = limit_recommended
    resp = requests_with_catching.get(base_url, params=dict_params, private_keys=['k'])
    tastedive_dict_movies = resp.json()
    return tastedive_dict_movies


def extract_movie_titles(tastedive_dict):
    """
    Takes and TasteDive dictionary object a returns a list with the names of
    the movies in it.
    """
    lst_dictionary_movies = tastedive_dict['Similar']['Results']
    movie_names_lst = [ movie['Name'] for movie in lst_dictionary_movies]
    return movie_names_lst


def get_related_titles(movie_titles_lst):
    """
    Takes a list of movie titles and returns a list of all the movies related
    to those titles
    """
    related_movies_so_far = []
    for title in movie_titles_lst:
        movies_rel_to_title = get_movies_from_tastedive(title)
        movie_titles_rel_to_title = extract_movie_titles(movies_rel_to_title)
        related_movies_so_far += movie_titles_rel_to_title
    # Making the list UNIQUE, in case a movie is repeated on the list
    related_movies = list(set(related_movies_so_far))
    return related_movies


def get_movie_data(movie_title, apikey=OMDBAPI_KEY, type='movies', r='json'):
    base_url = 'http://www.omdbapi.com/'
    dict_params = {}
    # parameter apikey: API key to make queries.
    dict_params['apikey'] = apikey
    # parameter t: Movie title to search for.
    dict_params['t'] = movie_title
    # parameter type: Type of result to return.
    dict_params['type'] = type
    # paramater r: The data type to return.
    dict_params['r'] = r
    resp = requests_with_catching.get(base_url, params=dict_params, private_keys=['apikey'])
    omdb_dict_data = resp.json()
    return omdb_dict_data


def get_movie_rating(omdb_dict, source='Rotten Tomatoes'):
    ratings = omdb_dict['Ratings']
    for rating in ratings:
        if rating['Source'] == source:
            if source == 'Internet Movie Database':
                return float(rating['Value`'][:3])
            elif source == 'Rotten Tomatoes':
                return float(rating['Value'][:-1])
            elif source == 'Metacritic':
                return float(rating['Value'][:2])
    return 0.0


def get_sorted_recommendations(movie_titles_lst):
    related_movie_lst = get_related_titles(movie_titles_lst)
    related_movies_rating = []
    for movie in related_movie_lst:
        movie_data = get_movie_data(movie)
        movie_rating = get_movie_rating(movie_data)
        related_movies_rating.append((movie_rating, movie))
    # Sorting for Highest to lowest rating.
    # In case of tie, inverse alphabetical order
    sorted_movies_rating = sorted(related_movies_rating)
    # Only need the titles
    sorted_recommendations = [movie for (rating, movie) in sorted_movies_rating]
    return sorted_recommendations
