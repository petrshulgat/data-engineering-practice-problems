import requests 
import pandas as pd
from bs4 import BeautifulSoup

url = 'https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/'

target_file = None

def main():
    
    page = requests.get(url).text 
    data = BeautifulSoup(page, 'html.parser')

    rows = data.find_all('tr')

    for row in rows:
        cells = row.find_all('td')

        if len(cells) > 1:
            last_modified = cells[1].text 

            if last_modified == '2026-03-23 13:10':
                 target_file = cells[0].find('a')['href']
                 break

    if target_file:
        file_url = url + target_file

        response = requests.get(file_url)

        with open(target_file, 'wb') as f:
            f.write(response.content)
    else:
        print('No file')

        
    df = pd.read_csv(target_file)
    max_damage = df['DAMAGE_PROPERTY'].max()
    result = df[df['DAMAGE_PROPERTY'] == max_damage]

    print(result)

    



if __name__ == '__main__':
    main()