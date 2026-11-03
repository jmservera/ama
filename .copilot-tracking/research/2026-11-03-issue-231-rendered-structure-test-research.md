# Research: issue #231 slice 6, rendered structure test

Task: issue-231-rendered-structure-test. Disposition: executed (reuses prior #231 research). Planning Readiness: Ready.

## Merged delivery checked

* #656 technical and quality queue screens; #769 browser keyboard and axe evidence; #807 source conflicts; #828 incomplete sign-offs; #886 quality acceptance and ownerless defects. Closed #494 superseded.
* Issue criteria 1 to 3 are checked and proven by those PRs.

## Unmet criteria

* 4 WCAG 2.2 baseline: engineering evidence exists (#769) but assistive-technology and user validation (#155) is human work and not run.
* 5 Design system components (#150): source-level class and no-simulator tests exist (test_role_screens, test_role_screens_conformance). Adoption of an actual Fluent implementation needs packaging, CSP and owner decisions; not a small slice.

## Gap found

Existing class and simulator checks read the JS source. No test checks the rendered technical and quality trees in ready, blocked and empty states.

## Slice

Add rendered-tree tests: classes subset of the #150 inventory, no role simulator text, headings, sections and table captions present. Test only; no behaviour change.
