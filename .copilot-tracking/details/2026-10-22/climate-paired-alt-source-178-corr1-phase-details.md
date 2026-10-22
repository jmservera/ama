<!-- markdownlint-disable-file -->

# Phase details: climate-paired-alt-source-178-corr1

* P01: _monthly_extremes in tools/climate_paired_bounds.py groups record indices by UTC month; per month and variable it records value and occurrences (time, paired value of the other variable) for every record equal to the extremum, in input (chronological) order. Report regenerated with the documented command (stdout to the report file). Tests: split-month tie case, paired provenance, golden regeneration from fixtures, monthly versus annual reconciliation (12 months, same value and same timestamps).
* P02: one paragraph in the IoT synthesis reproduction section; log entry appended.
* P03: gate on the committed head; external receipt; verifier before push.

## Correction 2 (RV-001)

* P04: add helper _object(value, label) raising ValueError "<label> must be a JSON object"; use it for hourly_units, header, parameters (and the T2M and RH2M entries), properties, parameter and geometry. Absent keys keep prior behaviour. geometry.coordinates must be a list. Validation intent: regressions with array, scalar and null values for each container in each parser must raise ValueError and never AttributeError; the committed-fixture golden test passes unchanged; a mutation check removing the helper must fail the new tests.
* P05: coordinator-owned gate and publication.
