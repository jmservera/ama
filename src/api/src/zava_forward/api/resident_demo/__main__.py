"""Start the synthetic resident showcase: python -m zava_forward.api.resident_demo.

Configuration comes only from ZF_DEMO_* and ZF_SQL_* settings (see core/resident_showcase.py).
It refuses to start on any missing, expired, mixed (staff, Entra, AI) or unsafe setting, or when
the SQL allowlist view admits no resident. It never reads the password, only its scrypt verifier.
"""

import os
import sys
from datetime import UTC, datetime

from zava_forward.core import resident_showcase as rs
from zava_forward.core import resident_showcase_sql as rsql

from .app import ResidentDemo, serve


def main() -> int:
    try:
        config = rs.config_from_env(os.environ)
        reader = rsql.ShowcaseReader(rsql.connector(config.sql))
        identity = rs.build_identity_map(reader.list_rows(), datetime.now(UTC))
        if not identity.cases:
            raise rs.ShowcaseConfigError("The allowlist view admits no showcase resident.")
    except rs.ShowcaseConfigError as error:
        print(f"Refusing to start: {error}", file=sys.stderr)
        return 2
    except Exception as error:
        print(f"Refusing to start: SQL read failed ({type(error).__name__}).", file=sys.stderr)
        return 2
    app = ResidentDemo(
        reader,
        identity,
        config.verifier,
        rs.SessionCodec(config.session_key, config.expires_at),
        rs.LoginLimiter(),
        config.allowed_hosts,
        config.expires_at,
        config.bind,
        config.port,
    )
    server = serve(app)
    print(
        f"Synthetic resident showcase on {config.bind}:{app.port} until "
        f"{config.expires_at.isoformat()}; {len(identity.cases)} residents admitted "
        f"({sum(identity.excluded.values())} excluded)",
        flush=True,
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
