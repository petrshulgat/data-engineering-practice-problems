# Python Data Engineering Exercises
> Practice working with `requests`, `json`, and `csv` — the core tools of real data pipelines.

These three exercises follow the full data engineering loop: **fetch → parse → transform → store → report**.  
Do them in order. Exercise 3 is significantly harder than it looks without pandas.

---

## Exercise 1 — Fetch & Save JSON from a Public API

### Goal
Pull live weather data from a public API, extract specific fields, and persist them as JSON files.

### Setup
[Open-Meteo](https://open-meteo.com/) is free and requires no API key.

Use the following cities:

```python
cities = [
    {"name": "Budapest", "lat": 47.4979, "lon": 19.0402},
    {"name": "London",   "lat": 51.5074, "lon": -0.1278},
    {"name": "New York", "lat": 40.7128, "lon": -74.0060},
    {"name": "Tokyo",    "lat": 35.6762, "lon": 139.6503},
    {"name": "Sydney",   "lat": -33.8688, "lon": 151.2093},
]
```

URL pattern:
```
https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true
```

### Tasks
1. Create a folder called `weather_data` if it doesn't exist
2. Fetch current weather for each city using the URL pattern above
3. Parse the JSON response and extract only: `city name`, `temperature`, `windspeed`, `time`
4. Save each city's data as a separate `.json` file named after the city (e.g. `budapest.json`)
5. Write a second function that reads all `.json` files back and prints a summary table to the console

### Expected output
```
weather_data/
├── budapest.json
├── london.json
├── new_york.json
├── tokyo.json
└── sydney.json
```

```
City        Temp (°C)   Wind (km/h)   Time
----------  ---------   -----------   -------------------
Budapest    18.3        12.4          2024-06-01T14:00
London      15.1        20.0          2024-06-01T13:00
...
```

### Skills practiced
`requests` · `json` · `os.makedirs` · file I/O · JSON parsing

### Extra credit
- [ ] Handle HTTP errors with `raise_for_status()`
- [ ] Fetch all 5 cities concurrently using `ThreadPoolExecutor`
- [ ] Add a unit test that mocks the API response using `unittest.mock`

---

## Exercise 2 — Paginated API to CSV

### Goal
Chain multiple API calls together, flatten nested JSON, and write the result to a CSV without using pandas.

### Setup
[JSONPlaceholder](https://jsonplaceholder.typicode.com) is a free fake REST API — no sign-up needed.

- Posts endpoint: `https://jsonplaceholder.typicode.com/posts`
- Comments endpoint: `https://jsonplaceholder.typicode.com/posts/{id}/comments`

### Tasks
1. Fetch all posts from the posts endpoint (returns 100 posts as JSON)
2. For each post, fetch its comments from the comments endpoint
3. Flatten the data so each row contains:

| Field | Source |
|---|---|
| `post_id` | post |
| `post_title` | post |
| `comment_id` | comment |
| `commenter_email` | comment |
| `comment_body` | comment |

4. Save the result to `posts_with_comments.csv` using the `csv` module (not pandas)
5. Print how many total rows were written

### Expected output
```
posts_with_comments.csv  (500 rows — 100 posts × 5 comments each)

post_id,post_title,comment_id,commenter_email,comment_body
1,sunt aut facere...,1,Eliseo@gardner.biz,laudantium enim...
1,sunt aut facere...,2,Jayne_Kuhic@sydney.com,est natus enim...
...
```

### Skills practiced
`requests` · `json` · `csv.DictWriter` · nested API calls · data flattening

### Extra credit
- [ ] Add a `time.sleep(0.1)` between comment requests to simulate rate limiting
- [ ] Wrap each request in a retry loop (try 3 times before giving up)
- [ ] Use `aiohttp` to fetch all comments concurrently instead

---

## Exercise 3 — CSV Download, Clean & Report

### Goal
Build a mini pipeline: download raw data, clean it using only the standard library, and produce a structured JSON report.

### Setup
Download this public CSV of world population data:
```
https://raw.githubusercontent.com/datasets/population/master/data/population.csv
```

### Tasks
1. Download the CSV and save it as `raw_population.csv` inside a folder called `pipeline`
2. Using **only the `csv` module** (no pandas), clean and transform the data:
   - Filter rows to only keep year `2000` and later
   - Remove any rows where population is missing or zero
   - Rename columns to: `country`, `country_code`, `year`, `population`
3. Save the cleaned data to `clean_population.csv`
4. From the cleaned data, produce a summary file called `report.json`:

```json
{
  "total_countries": 195,
  "year_range": { "min": 2000, "max": 2023 },
  "top_5_population_2023": [
    { "country": "India",  "population": 1428627663 },
    { "country": "China",  "population": 1425671352 },
    { "country": "USA",    "population": 339996563  },
    { "country": "Indonesia", "population": 277534122 },
    { "country": "Pakistan",  "population": 240485658 }
  ]
}
```

### Expected output
```
pipeline/
├── raw_population.csv
├── clean_population.csv
└── report.json
```

### Skills practiced
`requests` · `csv.reader` · `csv.DictWriter` · `json` · data cleaning · aggregation without pandas

### Extra credit
- [ ] Enrich each row with country metadata (capital, region) fetched from:  
  `https://restcountries.com/v3.1/alpha/{country_code}`
- [ ] Write a unit test for your cleaning logic using a small hand-written CSV string and `io.StringIO`
- [ ] Add a step that detects and logs duplicate rows before cleaning

---

## Skills Reference

| Library | Key things to know |
|---|---|
| `requests` | `.get()`, `.raise_for_status()`, `.json()`, `.text`, `.headers` |
| `json` | `json.loads()`, `json.dumps()`, `json.load(f)`, `json.dump(obj, f)` |
| `csv` | `csv.reader()`, `csv.DictReader()`, `csv.writer()`, `csv.DictWriter()` |
| `os` | `os.makedirs(path, exist_ok=True)`, `os.path.join()`, `os.listdir()` |
