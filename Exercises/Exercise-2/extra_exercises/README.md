# Web Scraping & Pandas Practice Tasks

---

## Task 1 — NOAA Storm Events Data

### Problem Statement

You need to download a file of storm event data from a government website. Files are located at:

**`https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/`**

You are looking for the file that was `Last Modified` on `2024-01-26 13:10`. You **cannot** look up the filename yourself — you must use Python to scrape the webpage and find the corresponding filename for this timestamp.

Once you have the correct file downloaded, load it into Pandas and find the record(s) with the **highest `DAMAGE_PROPERTY` value**. Print these records to the command line.

---

### Steps

**Step 1 — Scrape the directory page**

```python
import requests
from bs4 import BeautifulSoup

url = 'https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/'
page = requests.get(url).text
soup = BeautifulSoup(page, 'html.parser')
```

Fetch the contents of the directory listing page and parse it using BeautifulSoup.

---

**Step 2 — Analyse the structure and find the target file**

Inspect the HTML table rows to locate the file where the `Last Modified` column matches `2024-01-26 13:10`.

```python
rows = soup.find_all('tr')
target_file = None

for row in rows:
    cells = row.find_all('td')
    if len(cells) >= 2:
        last_modified = cells[1].text.strip()
        if last_modified == '2024-01-26 13:10':
            target_file = cells[0].find('a')['href']
            break
```

---

**Step 3 — Build the URL and download the file**

```python
if target_file:
    file_url = url + target_file
    response = requests.get(file_url)
    with open(target_file, 'wb') as f:
        f.write(response.content)
```

Construct the full download URL by appending the filename to the base URL. Save the file locally using binary write mode (`'wb'`).

---

**Step 4 — Load into Pandas and find the maximum**

```python
import pandas as pd

df = pd.read_csv(target_file)
max_damage = df['DAMAGE_PROPERTY'].max()
result = df[df['DAMAGE_PROPERTY'] == max_damage]
```

Read the CSV file into a DataFrame and filter for the row(s) with the highest property damage value.

---

**Step 5 — Print results to the terminal**

```python
print(result)
```

---

