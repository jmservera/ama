import hashlib
import sys
from pathlib import Path

from zava_forward.core.synthetic import provenance

p = Path(provenance.__file__).resolve()
print("python", sys.executable)
print("prefix", sys.prefix)
print("helper_path", p)
print("helper_sha256", hashlib.sha256(p.read_bytes()).hexdigest())
