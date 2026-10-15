# Details: issue 200

* `build_mvp_dataset.py`: import `output_dir` from `zava_forward.core.synthetic`; default `--out` is `output_dir("zavaforward.json")`; remove `REPO` and the `mvp` path insert.
* `mvp-validation.yml`: `git ls-files mvp/data ':(glob)src/**/data/**'` must be empty.
* No new code in `mvp/`; workflow names unchanged.
