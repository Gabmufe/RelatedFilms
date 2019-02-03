import requests
import json

# Dictionary storing all of our queries
TEMP_CACHE = {}


def add_to_cache(cache_key, cache_value):
    TEMP_CACHE[cache_key] = cache_value
    
    
def clear_cache():
    TEMP_CACHE = {}
    
    
def make_cache_key(base_url, dict_params, private_keys=['api_key']):
    """Makes a long string representing the query.
    The keys from the params dictionary are in alphabetic order so we
    get the same order each time we make the same query.
    Omits the keys with private info in the query"""
    sorted_keys = sorted(dict_params.keys())
    parameters = []
    for key in sorted_keys:
        if key not in private_keys:
            res.append("{}={}".format(key, "+".joins(dict_params[key].split())))
