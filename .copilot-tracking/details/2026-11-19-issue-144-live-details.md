# Details
Input shape: JSON array of resources with `name` and `properties.template.containers[].image`. Output: JSON report per container with `kind` in {digest-pinned, tag-only, latest, placeholder, foreign-registry}. `--registry` sets the expected login server; `--tags` optional JSON map repo to tag list is not required. Nonzero exit unless all are digest-pinned on the expected registry.
