# Research: role-screens.js syntax break on main

Evidence: node --check fails on main; src-api tests fail on every open PR. Bisect of git log for role-screens.js shows the PR #652 to #655 branches already lacked closing lines for four registerRoleScreen blocks (contractor-job-pack, data-operator, hazard-triage region, resident-choice), lost in automated conflict resolution. Intact tails from commits 1df497e5, 2b9fd29a, 6cb506f4.
