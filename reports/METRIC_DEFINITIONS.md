# Metric definitions and report grain

| Metric | Definition | Denominator / grain |
| --- | --- | --- |
| Inspection records | Count of unique `Inspection ID` | One source row per inspection event |
| Outcome-eligible inspections | Count where `Result` is `Pass`, `Pass w/ Conditions`, or `Fail` | Inspection events with one of those three outcomes |
| Failures | Count where `Result = Fail` | Inspection events |
| Observed failure rate | Failures / outcome-eligible inspections | Outcome-eligible events only |
| Pass with conditions | Count where `Result = Pass w/ Conditions` | Inspection events; shown separately from unqualified Pass |
| Other results | Count of all remaining result values | Inspection events; not assumed to be passes |

`Month Start` is a calendar-month date for trend sorting. `Inspection Group` groups the source inspection type into Canvass, Complaint, License, their reinspections, and Other. `Facility Group` preserves the four most common named categories and combines all remaining or blank values into Other / not recorded. Original source fields remain unchanged in the local raw extract.

Rate comparisons use **inspection events**, so they should not be described as the percentage of establishments failing. Multiple inspection events can belong to one establishment. Reinspections are follow-up events, not a random sample comparable to initial inspections.

