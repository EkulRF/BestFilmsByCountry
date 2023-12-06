# Best Films by Country

Using [The Movie Database API](https://developer.themoviedb.org/reference/intro/getting-started) to map out the top-rated movie made in each country.

## Information

### How do you get the "top movie" from a country?

Using the "discover" API from The Movie Database (TMDB) <`https://developer.themoviedb.org/reference/discover-movie`> with query parameters:

| parameter | value | description |
| --- | --- | --- |
| `sort_by` | `vote_average.desc` | sort by average vote (the highest first) |
| `with_origin_country` | `${iso 3166 1 country code!}` | the country in question! |
| `vote_count.gte` | variable | This behaviour copies the [top-rated] API behaviour. We start at 200, and step down to get less noisy results. |

[top-rated]: https://developer.themoviedb.org/reference/movie-top-rated-list

### How to get movie images

Each movie returns a `backdrop_path` and `poster_path`. Broadly, the backdrop is landscape, and the poster portrait. You can combine these with data from the [details API]

[details API]: https://developer.themoviedb.org/reference/configuration-details

```json
{
"base_url": "http://image.tmdb.org/t/p/",
"secure_base_url": "https://image.tmdb.org/t/p/",
"backdrop_sizes": [
    "w300",
    "w780",
    "w1280",
    "original"
],
"logo_sizes": [
    "w45",
    "w92",
    "w154",
    "w185",
    "w300",
    "w500",
    "original"
],
"poster_sizes": [
    "w92",
    "w154",
    "w185",
    "w342",
    "w500",
    "w780",
    "original"
]
}
```

So, for example, The Godfather's images could be, from

```json
{
  "backdrop_path": "/tmU7GeKVybMWFButWEGl2M4GeiP.jpg",
  "poster_path": "/3bhkrj58Vtu7enYsRolD1fZdja1.jpg",
}
```

```text
https://image.tmdb.org/t/p/original/tmU7GeKVybMWFButWEGl2M4GeiP.jpg
https://image.tmdb.org/t/p/original/3bhkrj58Vtu7enYsRolD1fZdja1.jpg
```

## Development (data collection)

### Get API key

[Get an API key](https://developer.themoviedb.org/reference/intro/authentication#api-key-quick-start) for TMDB. Put this in `.env` file

```bash
echo "TMDB_KEY=82u489u284282" > .env
```

```.env
TMDB_KEY=82u489u284282
```

### Install dependencies

```bash
python -m venv env
# activate venv (platform dependent)
pip install -r requirements.txt
```

### Fetch movie data from TMDB API

```bash
python get_movies.py
```

Data is saved to `countries.json`. A few countries do not have data. See which ones by [running the script](#fetch-movie-data-from-tmdb-api).

```json
[
    {"iso_3166_1": "AD", "english_name": "Andorra", "native_name": "Andorra", "top_movie": null},
    {"iso_3166_1": "AE", "english_name": "United Arab Emirates", "native_name": "United Arab Emirates", "top_movie": {"id": 89708, "title": "Samsara", "original_title": "Samsara", "original_language": "en", "release_date": "2011-09-16", "genre_ids": [99], "overview": "Filmed over nearly five years in twenty-five countries on five continents, and shot on seventy-millimetre film, Samsara transports us to the varied worlds of sacred grounds, disaster zones, industrial complexes, and natural wonders.", "vote_average": 8.1, "vote_count": 564, "popularity": 12.409, "backdrop_path": "/2pawKej1ZZfbbpfJfvj5R8q9NhC.jpg", "poster_path": "/qodkea4k0pNUmNTl5TJO2PdTqgW.jpg", "video": false, "adult": false}}
    {"iso_3166_1": "AL", "english_name": "Albania", "native_name": "Albania", "top_movie": {"id": 763788, "title": "Dangerous", "original_title": "Dangerous", "original_language": "en", "release_date": "2021-11-05", "genre_ids": [28, 53], "overview": "A reformed sociopath heads to a remote island after the death of his brother. Soon after his arrival, the island falls under siege from a deadly gang of mercenaries, and when he discovers their role in his brother\u2019s demise, he sets out on a relentless quest for vengeance.", "vote_average": 6.2, "vote_count": 386, "popularity": 27.343, "backdrop_path": "/mo57hzhW3BcZL1f7MNteWKHsmlN.jpg", "poster_path": "/vTtkQGC7qKlSRQJZYtAWAmYdH0A.jpg", "video": false, "adult": false}}
]
```

## Development (frontend)

The library for the SVG map is <https://jvectormap.com>.
