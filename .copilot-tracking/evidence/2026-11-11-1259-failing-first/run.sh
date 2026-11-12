#!/bin/sh
# usage: run.sh <export-name> <logfile>
S=/home/azureuser/.local/share/ama/gates/g1259-ff-2122
cd $S/$1/src/core || exit 99
export_env() { env -i HOME=$S/home PATH=/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:tests ZF_DATA=$S/data/zavaforward.json TMPDIR=$S/tmp "$@"; }
{
echo "date $(date -u +%FT%TZ) export=$1 cwd=$(pwd)"
export_env python3 -S -c "import zava_forward.core.ranking_publication as a, zava_forward.core.ranking_publication_runner as b, zava_forward.core.store as c; print(a.__file__); print(b.__file__); print(c.__file__)"
echo "origin_exit=$?"
export_env python3 -S -m unittest -v \
 test_ranking_publication_runner.UnusableArchivePathTests \
 test_ranking_publication_runner.StorageAndDuplicateFindingTests.test_unreadable_archive_is_a_problem_never_empty_or_healthy \
 test_ranking_publication_runner.StorageAndDuplicateFindingTests.test_unreadable_archive_exits_nonzero_through_main
echo "unittest_exit=$?"
} > $2 2>&1
