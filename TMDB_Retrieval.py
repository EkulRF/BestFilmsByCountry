"""load data from The Movie Database (TMDB) to get the "top film per country" datasset"""
import os
import sys
import pickle
import requests
from tqdm import tqdm

from dotenv import load_dotenv

load_dotenv()

# 4fad2cdfc5ea0c55513d2d7cbe65f25e

api_key = os.environ["TMDB_KEY"]
BASE_URL = "https://api.themoviedb.org/3"


def get_top_rated_movies_onpage(page):
    endpoint = "/movie/top_rated"
    params = {
        "api_key": api_key,
        "page": page,
    }

    response = requests.get(BASE_URL + endpoint, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print(f"Error: {response.status_code}")
        return ["None"]


def get_highest_rated_movies(num_pages):
    all_top_rated_movies = []

    for page in tqdm(range(1, num_pages + 1)):
        top_rated_movies = get_top_rated_movies_onpage(page)
        all_top_rated_movies.extend(top_rated_movies)

    # Filter top rated movies by the specified country of origin
    print("Extracting Country of Origin")
    for i in tqdm(range(len(all_top_rated_movies))):
        all_top_rated_movies[i]["country"] = get_movie_details(
            api_key, all_top_rated_movies[i]["title"]
        )

    return all_top_rated_movies


def get_movie_details(api_key, movie_title):
    base_url = "https://api.themoviedb.org/3/search/movie"
    params = {"api_key": api_key, "query": movie_title}

    response = requests.get(base_url, params=params)
    data = response.json()

    if data["results"]:
        # Assuming the first result is the most relevant
        movie_id = data["results"][0]["id"]
        return get_movie_country(api_key, movie_id)
    else:
        return ["None"]


def get_movie_country(api_key, movie_id):
    base_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        "api_key": api_key,
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if "production_countries" in data:
        if len(data["production_countries"]) == 0:
            return ["None"]
        else:
            countries = [country["name"] for country in data["production_countries"]]
        return countries
    else:
        return ["None"]


def sort_movies_by_country(original_dict):
    print("Sorting!")
    sorted_dict = {}

    for entry in original_dict:
        countries = entry["country"]

        for country in countries:
            if country not in sorted_dict:
                sorted_dict[country] = {"movies": []}

            sorted_dict[country]["movies"].append(entry)

    return sorted_dict


def main(num_top: int):
    """main"""
    highest_rated_movies = get_highest_rated_movies(num_top)

    _sorted = sort_movies_by_country(highest_rated_movies)

    with open("HighRankedMovies_ByCountry.pickle", "wb") as handle:
        pickle.dump(_sorted, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print(_sorted.keys())


if __name__ == "__main__":
    if len(sys.argv) == 2:
        _num_top = int(sys.argv[1])
    else:
        print("Usage: python3 TMDB_Retrieval.py <num_top_films>")
        sys.exit(1)
    main(_num_top)
