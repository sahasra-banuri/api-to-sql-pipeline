import requests
import json

from pathlib import Path
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


API_URL = "https://dummyjson.com/carts"


def ingest_data():

    # Step 1: Configure retry strategy
    retry_strategy = Retry(
        total=3,
        connect=3,
        read=3,
        status=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods={"GET"},
        respect_retry_after_header=True
    )

    # Step 2: Configure HTTP session
    adapter = HTTPAdapter(max_retries=retry_strategy)

    with requests.Session() as session:

        session.mount("https://", adapter)

        # Step 3: Send GET request
        response = session.get(API_URL, timeout=30)

        # Step 4: Check request status
        response.raise_for_status()

        # Step 5: Convert JSON response
        data = response.json()

    # Step 6: Save raw data
    raw_folder = Path("data/raw")
    raw_folder.mkdir(parents=True, exist_ok=True)

    output_file = raw_folder / "carts.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print("API data successfully retrieved.")
    print(f"Number of carts: {len(data['carts'])}")
    print(f"Raw data saved to: {output_file}")

    return data


if __name__ == "__main__":
    ingest_data()