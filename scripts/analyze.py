"""Create a Power BI-ready table and independently checked inspection summaries."""
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
import csv
import json

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "inspections_2024_2025.csv"
OUTPUT = ROOT / "data" / "inspections_analysis.csv"
ANALYSIS = ROOT / "analysis"
ANALYSIS.mkdir(exist_ok=True)

OUTCOMES = {"Pass", "Pass w/ Conditions", "Fail"}
FACILITIES = {"Restaurant", "Grocery Store", "School", "Children's Services Facility"}


def type_group(value):
    if value.startswith("Canvass"):
        return "Canvass reinspection" if "Re-Inspection" in value else "Canvass"
    if value.startswith("Complaint"):
        return "Complaint reinspection" if "Re-Inspection" in value else "Complaint"
    if value.startswith("License"):
        return "License reinspection" if "Re-Inspection" in value else "License"
    return "Other inspection type"


def summarize(rows):
    eligible = [row for row in rows if row["Outcome Eligible"] == "Yes"]
    failures = sum(row["Result"] == "Fail" for row in eligible)
    return {
        "inspections": len(rows),
        "outcome_eligible": len(eligible),
        "failures": failures,
        "failure_rate": round(failures / len(eligible), 6) if eligible else None,
        "pass_with_conditions": sum(row["Result"] == "Pass w/ Conditions" for row in eligible),
        "other_results": len(rows) - len(eligible),
    }


with SOURCE.open(newline="", encoding="utf-8-sig") as handle:
    raw = list(csv.DictReader(handle))

ids = [row["inspection_id"] for row in raw]
if len(set(ids)) != len(ids):
    raise ValueError("Duplicate inspection IDs in source extract")

clean = []
for row in raw:
    date = datetime.fromisoformat(row["inspection_date"][:10])
    result = row["results"].strip()
    facility = row["facility_type"].strip()
    clean.append({
        "Inspection ID": row["inspection_id"],
        "Inspection Date": date.strftime("%Y-%m-%d"),
        "Year": date.year,
        "Month Start": date.strftime("%Y-%m-01"),
        "Month": date.strftime("%b"),
        "Risk": row["risk"].strip() or "Not recorded",
        "Facility Group": facility if facility in FACILITIES else "Other / not recorded",
        "Inspection Group": type_group(row["inspection_type"].strip()),
        "Result": result,
        "Outcome Eligible": "Yes" if result in OUTCOMES else "No",
        "Failure Flag": 1 if result == "Fail" else 0,
        "ZIP": row["zip"].strip(),
    })

with OUTPUT.open("w", newline="", encoding="utf-8-sig") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(clean[0]))
    writer.writeheader()
    writer.writerows(clean)


def group_summary(key):
    grouped = defaultdict(list)
    for row in clean:
        grouped[str(row[key])].append(row)
    return {value: summarize(rows) for value, rows in sorted(grouped.items())}


summary = {
    "scope": "City of Chicago Food Inspections, inspection dates 2024-01-01 through 2025-12-31; retrieved 2026-10-30",
    "rows": len(clean),
    "unique_inspection_ids": len(set(ids)),
    "date_min": min(row["Inspection Date"] for row in clean),
    "date_max": max(row["Inspection Date"] for row in clean),
    "overall": summarize(clean),
    "by_year": group_summary("Year"),
    "by_risk": group_summary("Risk"),
    "by_facility_group": group_summary("Facility Group"),
    "by_inspection_group": group_summary("Inspection Group"),
    "by_month": group_summary("Month Start"),
    "result_counts": dict(Counter(row["Result"] for row in clean)),
    "missing_zip": sum(not row["ZIP"] for row in clean),
}
(ANALYSIS / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: summary[k] for k in ("rows", "overall", "by_year", "by_inspection_group", "by_risk", "missing_zip")}, indent=2))

