import sys, json, functools, http.server, threading
import pathlib
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[4]/'src/api/tests'))
import test_resident_sensor_chart_browser as t
from playwright.sync_api import sync_playwright
M = """({history, points, idx}) => {
  const metric = sensorMetrics[idx];
  const figure = sensorChart(history, metric, {points});
  document.body.appendChild(figure);
  const svg = figure.querySelector('svg');
  const hit=(a,b)=>a.left<b.right&&b.left<a.right&&a.top<b.bottom&&b.top<a.bottom;
  const texts=[...svg.querySelectorAll('text')]; const tb=texts.map(x=>x.getBoundingClientRect());
  const shapes=[...svg.querySelectorAll('circle.sensor-point,rect.sensor-forecast-point')];
  const on=[];
  shapes.forEach(s=>tb.forEach((b,i)=>{ if(hit(s.getBoundingClientRect(),b)) on.push([s.getAttribute('class'),texts[i].textContent]);}));
  const lines=[...svg.querySelectorAll('polyline')];
  return {labels:texts.map(x=>x.textContent), on, circles:svg.querySelectorAll('circle').length, sq:svg.querySelectorAll('rect').length};
}"""
page_html=t.harness()
class S(t.Handler):
    def do_GET(self):
        if self.path=="/h.html":
            b=page_html.encode(); self.send_response(200); self.send_header("Content-Type","text/html"); self.send_header("Content-Length",str(len(b))); self.end_headers(); self.wfile.write(b); return
        super().do_GET()
srv=http.server.ThreadingHTTPServer(("127.0.0.1",0),functools.partial(S,directory=str(t.WEB)))
threading.Thread(target=srv.serve_forever,daemon=True).start()
with sync_playwright() as p:
    b=p.chromium.launch()
    for name,(c,s) in {"dense":(288,5),"short":(6,30),"one":(1,30),"two":(2,30),"day":(48,30)}.items():
      for idx in (0,1):
        for hv in (50,5,95):
          h=t.history(c,s)
          for r in h: r["humidity_pct"]=hv; r["temperature_c"]=hv/2-5 if idx==0 else r["temperature_c"]
          pts=t.forecast_points(h)
          for q in pts: q["humidity_pct"]=hv; q["temperature_c"]=hv/2-5
          pg=b.new_page(viewport={"width":1440,"height":900}); pg.goto(f"http://127.0.0.1:{srv.server_port}/h.html")
          r=pg.evaluate(M,{"history":h,"points":pts,"idx":idx}); pg.close()
          if r["on"]: print(name,idx,hv,r["on"][:4])
    b.close()
print("done")
