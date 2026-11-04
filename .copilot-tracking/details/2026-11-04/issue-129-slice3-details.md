# Issue 129 slice 3 details

* run_report rejects a run that does not state representative_data_retained as false, so DPO-undecided retention is never implied.
* For bundles with O16 (change-impact, funding-evidence) the run must name the bundle that counts O16; other bundles must not.
* reconcile_o16 rejects runs that name different O16 owners, preventing double counting.
* render_report puts any STOP before effort figures and repeats the capacity and constructed-case labels.
