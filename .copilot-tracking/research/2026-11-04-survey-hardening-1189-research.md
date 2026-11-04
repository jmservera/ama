# Research: harden expected denials survey (Refs #1189)

* Merged PRs: #1188 added survey_role (the source of the review findings); no PR has addressed #1189.
* me payload carries the role at me.user.role as the mapped display name (auth.DEFAULT_ROLE_MAP), not me.role; navigation is me.navigation.
* Planning readiness: Ready. Single slice covers every acceptance criterion; no stacking needed.
