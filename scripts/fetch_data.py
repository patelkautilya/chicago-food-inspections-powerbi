"""Download a reproducible, bounded extract of Chicago food inspections."""
from pathlib import Path
import csv
import json
from urllib.parse import urlencode
from urllib.request import urlopen

BASE = "https://data.cityofchicago.org/resource/4ijn-s7e5.json"
WHERE = "inspection_date >= '2024-01-01T00:00:00' and inspection_date < '2026-01-01T00:00:00'"
FIELDS = [
    "inspection_id", "inspection_date", "facility_type", "risk",
    "inspection_type", "results", "zip",
]
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data"
OUT.mkdir(exist_ok=True)

def get_rows(params, timeout=120):
    with urlopen(BASE + "?" + urlencode(params), timeout=timeout) as response:
        return json.load(response)


expected = int(get_rows({"$select": "count(*) as n", "$where": WHERE})[0]["n"])

rows = []
limit = 50000
for offset in range(0, expected, limit):
    rows.extend(get_rows(
        {
            "$select": ",".join(FIELDS),
            "$where": WHERE,
            "$order": "inspection_date ASC, inspection_id ASC",
            "$limit": limit,
            "$offset": offset,
        }
    ))

if len(rows) != expected:
    raise RuntimeError(f"Expected {expected:,} rows; received {len(rows):,}")

with (OUT / "inspections_2024_2025.csv").open("w", newline="", encoding="utf-8-sig") as handle:
    writer = csv.DictWriter(handle, fieldnames=FIELDS)
    writer.writeheader()
    for row in rows:
        writer.writerow({field: row.get(field, "") for field in FIELDS})

metadata = {
    "source": "City of Chicago Food Inspections",
    "dataset_url": "https://data.cityofchicago.org/Health-Human-Services/Food-Inspections/4ijn-s7e5",
    "api_url": BASE,
    "where": WHERE,
    "fields": FIELDS,
    "source_row_count": expected,
    "downloaded_row_count": len(rows),
}
(OUT / "extract_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
print(json.dumps(metadata, indent=2))

