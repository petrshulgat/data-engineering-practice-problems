import json 
import csv 
import glob 
import pandas as pd
from pathlib import Path 


def main():
    
    dir = Path('data')

    for file in dir.rglob('*.json'):

        filename = file.with_suffix('.csv')

        with open(file, 'r') as f:
            data =  json.load(f)

        if isinstance(data, dict):
            data = [data]

        df = pd.json_normalize(data)

        with open(filename, 'w', newline='') as csvf:
            writer = csv.DictWriter(csvf, fieldnames=df.columns.tolist())
            writer.writeheader()
            writer.writerows(df.to_dict(orient='records'))



if __name__ == "__main__":
    main()
