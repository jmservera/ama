import sys

from zava_forward.core.version import __version__

if sys.argv[1:2] == ["discovery-demo"]:
    from zava_forward.core import discovery_assistant_demo

    raise SystemExit(discovery_assistant_demo.main(sys.argv[2:]))

print(f"zava-forward-core {__version__}")
