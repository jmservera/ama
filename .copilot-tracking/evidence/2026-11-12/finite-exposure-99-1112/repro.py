from datetime import date, timedelta
from zava_forward.core import exposure_limits as L
A=dict(approver="T",role="R",approved_on=(date.today()-timedelta(days=30)).isoformat(),evidence_ref="s",restart_owner="O")
rec=L.record_limits(A,dict(amount=100,currency="GBP",period="y"),dict(capital=dict(maximum=10,unit="percent"),safety=dict(maximum=0,unit="count")))
inf=float("inf");nan=float("nan")
cases={
 "committed=-inf,tol ok":dict(committed=-inf,currency="GBP",tolerances=dict(capital=1,safety=0)),
 "committed ok,tol=-inf":dict(committed=1,currency="GBP",tolerances=dict(capital=-inf,safety=-inf)),
 "all -inf":dict(committed=-inf,currency="GBP",tolerances=dict(capital=-inf,safety=-inf)),
 "committed=+inf":dict(committed=inf,currency="GBP",tolerances=dict(capital=1,safety=0)),
 "tol=+inf":dict(committed=1,currency="GBP",tolerances=dict(capital=inf,safety=0)),
 "committed=nan":dict(committed=nan,currency="GBP",tolerances=dict(capital=1,safety=0)),
 "tol=nan":dict(committed=1,currency="GBP",tolerances=dict(capital=nan,safety=0)),
}
for k,v in cases.items():
    r=L.assess(rec,v);print(f"{k:24} -> {r['status']} | {r['signal']} | {[f['state'] for f in r['findings']]}")
