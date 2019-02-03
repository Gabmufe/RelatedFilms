import requests
import json


"""
This is an auxiliar module that keeps a cache memory so once u made a query
you store the results in a file. This way u can use the same answer again and
again without worrying about changes in the answer of your query.
Only for testing purposes.
"""


#File keeping some queries for testing purposes
PERM_CACHE_FNAME = 'permanent_cache.txt'


def _write_to_file(cache, fname):
    with open(fname, 'w') as output_file:
        output_file.write(json.dumps(cache, indent=2))


def _read_from_file(fname):
    try:
        with open(fname, 'r') as input_file:
            resp_json = input_file.read()
            return json_loads(resp_json)
    except:
        return {}


def make_cache_key(base_url, dict_params, private_keys=['api_key']):
    """Makes a long string representing the query.
    The keys from the dictionary params are sorted in alphabetical order,
    so we get the same order each time.
    Omit the keys with private info."""
    sorted_keys = sorted(dict_params.keys())
    params = []
    for key in sorted_keys:
        if key not in private_keys:
            params.append("{}={}".format(key, "+".join(dict_params[key].split())))
    return base_url + '?' + "&".join(params)


def get(base_url, dict_params={}, private_keys=['api_key'], permanent_cache_file=PERM_CACHE_FNAME):
    full_url = requests.requestURL(base_url, dict_params)
    cache_key = make_cache_key(base_url, dictionary, private_keys)
    # Load the permanent caches from files
    permanent_cache = _read_from_file(permanent_cache_file)
    if cache_key in permanent_cache:
        # Make a Response object containing text from the change, and the full_url
        # that would have been fetched
        return requests.Response(permanent_cache[cache_key], full_url)
    else:
        # Actually request the query
        resp = request.get(base_url, dict_params)
        # Save it
        permanent_cache[cache_key] = resp.text
        _write_to_file(permanent_cache, PERM_CACHE_FNAME)
        return resp
