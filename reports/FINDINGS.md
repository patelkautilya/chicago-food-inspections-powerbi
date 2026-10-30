# Findings | Chicago Food Inspections, 2024–2025

## Executive readout

The extract contains **38,433 unique inspection records**. Of these, **32,055** have a Pass, Pass w/ Conditions, or Fail outcome. **6,872** of those outcome-eligible inspections failed, for an observed **21.44% failure rate**.

The 2025 rate (**21.11%**) was **0.65 percentage points lower** than the 2024 rate (**21.76%**). This is a descriptive change in recorded inspection events; the data does not isolate policy effects or changes in the mix of inspections.

## Where to look next

**Complaint inspections:** 1,120 failures across 3,092 outcome-eligible complaint inspections (**36.22%**), compared with 3,882 across 16,958 canvass inspections (**22.89%**). Complaint-triggered inspections likely select establishments differently. A useful next analysis would compare more similar facility, risk, and time groups before using this gap for resource planning.

**Follow-up context:** Canvass reinspections show 485 failures across 4,619 outcome-eligible events (**10.50%**). Reinspections follow earlier events and are not an independent control group. The lower rate is not evidence that reinspection itself caused improvement.

**Outcome coverage:** 6,378 records (**16.60%** of all inspections) have a result outside the three outcome categories. Most are `No Entry` (2,796) or `Out of Business` (2,721). Reporting these separately prevents an artificially low failure rate.

## Interpretation limits

- Results describe findings at the time of inspection; they are not a continuing safety rating for an establishment.
- The unit is an inspection, so repeat events for the same establishment appear separately.
- Facility and risk comparisons are affected by different inspection pathways, schedules, and case mix.
- ZIP-based patterns are deliberately not used to rank neighborhoods; inspection counts and establishment mix vary.
- The extract is a dated snapshot from a source that may be revised. A refresh can change counts.

## Reconciliation

The source API returned **38,433** records for the 2024–2025 window; the extract contains the same number and all inspection IDs are unique. The 2024 and 2025 rows sum to 38,433. The outcome-eligible and other-result counts sum to 38,433. All KPI and segment calculations are reproducible with [`scripts/analyze.py`](../scripts/analyze.py) and recorded in [`analysis/summary.json`](../analysis/summary.json).


