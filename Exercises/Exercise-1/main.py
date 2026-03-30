import requests
import zipfile
from pathlib import Path

download_uris = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",
]


def main():


    download_dir = Path("downloads")
    download_dir.mkdir(exist_ok=True)

    for url in download_uris:
        try:
            filename = url.split("/")[-1]
            zip_path = download_dir / filename

            with requests.get(url, stream=True, timeout=10) as response:
                response.raise_for_status()

                with open(zip_path, "wb") as f:
                    for chunk in response.iter_content(8192):
                        if chunk:
                            f.write(chunk)

            print(f"Downloaded: {filename}")

            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                for file in zip_ref.namelist():
                    if file.endswith(".csv"):
                        zip_ref.extract(file, download_dir)
                        print(f"Extracted: {file}")

            zip_path.unlink()

        except Exception as e:
            print("Error")


if __name__ == "__main__":
    main()