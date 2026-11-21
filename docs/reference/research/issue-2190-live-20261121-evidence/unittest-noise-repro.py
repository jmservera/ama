import logging, threading, time, unittest, sys
log=logging.getLogger("x"); log.addHandler(logging.StreamHandler(sys.stderr)); log.setLevel(logging.INFO)
stop=threading.Event()
def noise():
    while not stop.is_set():
        log.info("http-response GET /x status=200 done")
class NoiseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.t=threading.Thread(target=noise,daemon=True);cls.t.start()
    @classmethod
    def tearDownClass(cls): stop.set()
for i in range(300):
    setattr(NoiseTests,f"test_{i:03d}",lambda self: time.sleep(0.0005))
