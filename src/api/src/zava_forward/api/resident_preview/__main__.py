"""Start the synthetic resident preview: python -m zava_forward.api.resident_preview."""

import argparse
import os
import sys
from pathlib import Path

from zava_forward.core import resident_preview as rp

from .app import ResidentPreview, serve


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="zava-resident-preview", description=__doc__)
    parser.add_argument(
        "--build-fixture", metavar="NEW_DIR", help="build a synthetic fixture, then exit"
    )
    parser.add_argument("--data-dir", help="directory holding dataset.json and grants.json")
    parser.add_argument("--subject", help="fixture subject this server process represents")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8444)
    args = parser.parse_args(argv)
    try:
        if args.build_fixture:
            from zava_forward.core.synthetic.resident_preview_fixture import build

            if any(k.upper().startswith(rp.FORBIDDEN_ENV_PREFIXES) for k in os.environ):
                raise rp.PreviewConfigError(
                    "Build from a clean environment (no ZF_, AI_ or cloud settings)."
                )
            dataset, fixture = build(args.build_fixture)
            print(f"Built synthetic fixture:\n  {dataset}\n  {fixture}")
            return 0
        if not args.data_dir or not args.subject:
            parser.error("--data-dir and --subject are required")
        root = Path(args.data_dir)
        dataset, fixture = rp.safe_start(
            os.environ, root / "dataset.json", root / "grants.json", args.host
        )
        if args.subject not in rp.subjects(fixture):
            raise rp.PreviewConfigError("That subject is not in the synthetic fixture.")
        store, work = rp.open_store(dataset)
    except (rp.PreviewConfigError, rp.GrantDenied, OSError) as error:
        print(f"Refusing to start: {error}", file=sys.stderr)
        return 2
    app = ResidentPreview(store, fixture, args.subject, args.host, args.port)
    server = serve(app)
    shown = f"[{args.host}]" if ":" in args.host else args.host
    print(
        f"Synthetic resident preview (not live) at http://{shown}:{app.port}/ as {args.subject}",
        flush=True,
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        work.cleanup()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
