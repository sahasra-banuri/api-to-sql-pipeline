import requests
import json

from pathlib import Path
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


API_URL = "https://dummyjson.com/carts"


def ingest_data():

    # STEP 1: Configure retry mechanism

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

    adapter = HTTPAdapter(max_retries=retry_strategy)


    # STEP 2: Initialize pagination variables

    limit = 30
    skip = 0
    total = None

    all_carts = []


    # STEP 3: Fetch data page by page

    with requests.Session() as session:

        session.mount("https://", adapter)

        while total is None or skip < total:

            params = {
                "limit": limit,
                "skip": skip
            }

            response = session.get(
                API_URL,
                params=params,
                timeout=30
            )

            response.raise_for_status()

            page_data = response.json()

            # Read total records from API
            total = page_data["total"]

            # Retrieve carts from current page
            current_carts = page_data["carts"]

            # Add current page to our collection
            all_carts.extend(current_carts)

            print(
                f"Fetched {len(current_carts)} carts. "
                f"Total collected: {len(all_carts)}/{total}"
            )

            # Stop if API returns no more records
            if not current_carts:
                break

            # Move to next page
            skip += limit


    # STEP 4: Combine all pages into one response

    data = {
        "carts": all_carts,
        "total": total,
        "skip": 0,
        "limit": limit
    }


    # STEP 5: Save raw JSON

    raw_folder = Path("data/raw")
    raw_folder.mkdir(parents=True, exist_ok=True)

    output_file = raw_folder / "carts.json"

    with open(output_file, "w", encoding="utf-8") as file:

        json.dump(
            data,
            file,
            indent=4
        )


    print("\nAPI data successfully retrieved.")
    print(f"Total carts collected: {len(all_carts)}")
    print(f"Raw data saved to: {output_file}")

    return data


if __name__ == "__main__":
    ingest_data()