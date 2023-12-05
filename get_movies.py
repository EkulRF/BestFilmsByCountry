"""Load best movies from TMDB API and save them to a CSV file."""
import os
from dataclasses import dataclass
import json
import datetime
import pprint
from typing import List, Optional
import requests
from dotenv import load_dotenv
from tqdm import tqdm
from dataclasses_json import dataclass_json

SAVE_TO = "countries.json"

load_dotenv()

api_key = os.environ["TMDB_KEY"]


@dataclass_json
@dataclass
class Movie:
    """data returned from TMDB for each movie"""

    id: int
    title: str
    original_title: str
    original_language: str
    genre_ids: List[int]
    overview: str
    vote_average: float
    vote_count: int
    popularity: float
    backdrop_path: str
    poster_path: str
    video: bool
    adult: bool
    release_date: Optional[str] = None


@dataclass_json
@dataclass
class Country:
    """data for each country, including (eventually) the top movie"""

    iso_3166_1: str
    english_name: str
    native_name: str

    top_movie: Optional[Movie] = None


def main():
    """main"""

    print("getting all countries...")
    response = requests.get(
        "https://api.themoviedb.org/3/configuration/countries",
        params={
            "language": "en-US",
            "api_key": api_key,
        },
        timeout=5,
    )

    if response.status_code != 200:
        raise requests.HTTPError(response.status_code)
    countries = [Country(**country) for country in json.loads(response.text)]
    print(f"found {len(countries)} countries")

    print("getting top film for each country...")

    pbar = tqdm(countries)
    no_movies = []
    for country in pbar:
        pbar.set_description(f"getting top film for {country.english_name}...")
        for min_vote_count in [200, 100, 50, 10, 0]:
            response = requests.get(
                "https://api.themoviedb.org/3/discover/movie",
                params={
                    "language": "en-US",
                    "api_key": api_key,
                    "page": 1,
                    "sort_by": "vote_average.desc",
                    "with_origin_country": country.iso_3166_1,
                    "vote_count.gte": min_vote_count,
                    # "without_genres": "99,10755", # exclude documentaries and ???
                },
                timeout=5,
            )

            if response.status_code != 200:
                raise requests.HTTPError(response.status_code)
            response_json = json.loads(response.text)
            total_pages = response_json["total_pages"]
            total_results = response_json["total_results"]
            try:
                movies = [Movie(**movie) for movie in response_json["results"]]
            except TypeError as e:
                # missing data
                no_movies.append((country, e))

            if len(movies) > 0:
                country.top_movie = movies[0]
                break
        else:
            no_movies.append((country, "no movies found"))

    print("done")
    if no_movies:
        print(f"no movies found for {len(no_movies)} countries:")
        pprint.pprint(no_movies)

    print("saving to file...")
    countries_json = json.loads(Country.schema().dumps(countries, many=True))
    jsonfile = {
        "countries": countries_json,
        "last_modified": datetime.datetime.now().isoformat(),
    }
    with open(SAVE_TO, "w", encoding="utf-8") as f:
        json.dump(jsonfile, f, ensure_ascii=False, indent=2)
    # to load
    # Person.schema().loads(people_json, many=True)


if __name__ == "__main__":
    main()
