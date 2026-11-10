import json
from pathlib import Path
from datetime import datetime, timezone


def generate_data_quality_report(
    total_records,
    valid_records,
    rejected_records
):

    # Calculate record counts
    valid_count = len(valid_records)
    rejected_count = len(rejected_records)

    # Calculate quality percentages
    if total_records > 0:
        quality_rate = (valid_count / total_records) * 100
        rejection_rate = (rejected_count / total_records) * 100
    else:
        quality_rate = 0
        rejection_rate = 0

    # Calculate rejection reason breakdown
    if not rejected_records.empty:

        rejection_reasons = (
            rejected_records["rejection_reason"]
            .str.split(", ")
            .explode()
        )

        rejection_breakdown = (
            rejection_reasons.value_counts().to_dict()
        )

    else:
        rejection_breakdown = {}

    # Construct report
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),

        "summary": {
            "total_records": total_records,
            "valid_records": valid_count,
            "rejected_records": rejected_count,
            "data_quality_rate": round(quality_rate, 2),
            "rejection_rate": round(rejection_rate, 2)
        },

        "rejection_breakdown": rejection_breakdown
    }

    # Create reports directory
    report_folder = Path("data/reports")
    report_folder.mkdir(parents=True, exist_ok=True)

    # Save report
    report_file = report_folder / "data_quality_report.json"

    with open(report_file, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    print(f"Data quality report generated: {report_file}")

    return report