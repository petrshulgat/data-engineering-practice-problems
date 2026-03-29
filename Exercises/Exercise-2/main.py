import requests
import pandas as pd
from bs4 import BeautifulSoup


def main():
    url = 'https://www.ncei.noaa.gov/data/local-climatological-data/access/2021/'

    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')

    rows = soup.find_all('tr')

    target_file = None

    for row in rows:
        cells = row.find_all('td')

        if len(cells) >= 2:
            last_modified = cells[1].text.strip()

            if last_modified == '2024-01-19 15:10':
                target_file = cells[0].find('a')['href']
                break


    if target_file:
        file_url = url + target_file
        
        response = requests.get(file_url)
        with open(target_file, 'wb') as f:
            f.write(response.content)

        df = pd.read_csv(target_file)
        max_temperature = df['HourlyDryBulbTemperature'].max()
        result = df[df['HourlyDryBulbTemperature'] == max_temperature]

        print(result)

    else:
        print('No file')                                    




if __name__ == "__main__":
    main()
