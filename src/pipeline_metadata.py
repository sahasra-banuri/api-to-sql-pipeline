import json
import uuid
import time

from pathlib import Path
from datetime import datetime, timezone


def start_pipeline_run():

    run_metadata = {
        "run_id": str(uuid.uuid4()),

        "started_at": datetime.now(timezone.utc).isoformat(),

        "completed_at": None,

        "duration_seconds": None,

        "status": "RUNNING",

        "database_load_status": "NOT_STARTED",

        "records": {
            "carts_ingested": 0,
            "carts_transformed": 0,
            "products_transformed": 0,
            "valid_products": 0,
            "rejected_products": 0,
            "carts_submitted_for_loading": 0,
            "products_submitted_for_loading": 0
        },

        "error": None
    }

    start_time = time.perf_counter()

    return run_metadata, start_time


def finalize_pipeline_run(
    run_metadata,
    start_time,
    status,
    error=None
):

    end_time = time.perf_counter()

    run_metadata["completed_at"] = (
        datetime.now(timezone.utc).isoformat()
    )

    run_metadata["duration_seconds"] = round(
        end_time - start_time,
        3
    )

    run_metadata["status"] = status

    run_metadata["error"] = error

    # Create reports directory
    report_folder = Path("data/reports")
    report_folder.mkdir(parents=True, exist_ok=True)

    metadata_file = report_folder / "pipeline_runs.jsonl"

    # Append one execution record
    with open(metadata_file, "a", encoding="utf-8") as file:

        file.write(
            json.dumps(run_metadata) + "\n"
        )

    return run_metadata