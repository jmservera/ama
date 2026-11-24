import sys,time,cProfile,pstats,collections
sys.path[:0]=["src","tests","../core/src","../agents/src","../core/tests","../agents/tests"]
import unittest, test_assistants as t
class P(t.ForecastStatements):
    def runTest(self): pass
p=P(); p.setUp()
svc,seen=p.counted(443)
t0=time.time()
pr=cProfile.Profile(); pr.enable()
r=svc._forecast_compute(p.pm,86400)
pr.disable()
print("secs",time.time()-t0,"stmts",len(seen),"open",[a["open_cases_in_scope"] for a in r["assistants"]])
c=collections.Counter(" ".join(s.split())[:90] for s in seen)
for k,v in c.most_common(12): print(v,k)
pstats.Stats(pr).sort_stats("cumulative").print_stats(18)
