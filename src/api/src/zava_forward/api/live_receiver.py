"""Bounded host entry for the live synthetic receiver (issue 110 hosting glue for stage 2).

`python -m zava_forward.api.live_receiver --control-file F` reads the same control document as the
simulator, binds exactly that cohort (at most 100 homes, the `HubReceiver` limit) and runs one
finite receive window into the retained store, then exits. It starts nothing by itself: a manual
job trigger, an owner-verified routed Event Hub (`ZF_SIM_ROUTING_READY=1`) and an unexpired,
enabled control document are all required. It makes no model call and has no resident action.
"""

import argparse
import asyncio
import os
import sys
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path

from zava_forward.core.synthetic import sensor_identity
from zava_forward.core.synthetic.sensor_stream import StreamError

from . import live_control
from .iot_stream import Activation, Binding, HubReceiver
from .sensor_ingestion import SensorIngestion


def bindings(control: live_control.Control) -> tuple[Binding, ...]:
    """One `SYN-` device per cohort home, the same identity the simulator sends with."""
    result = []
    for home in control.homes:
        sensor = sensor_identity.sensor_key(home)
        result.append(Binding("SYN-" + sensor, sensor, home))
    return tuple(result)


def activation(env: Mapping[str, str], control: live_control.Control) -> Activation:
    hostname = env.get("ZF_SIM_HUB_HOSTNAME", "")
    namespace = "eh-" + hostname.removesuffix(".azure-devices.net") + ".servicebus.windows.net"
    return Activation(
        hub_hostname=hostname,
        eventhub_namespace=namespace,
        approval_reference=control.approval_reference,
        routing_ready=env.get("ZF_SIM_ROUTING_READY") == "1",
        managed_identity_client_id=env.get("ZF_SIM_CLIENT_ID") or None,
    )


async def run_window(
    control: live_control.Control,
    env: Mapping[str, str],
    ingestion: SensorIngestion,
    seconds: float,
    events: int,
    now: datetime,
    receiver_type: type[HubReceiver] = HubReceiver,
) -> int:
    """One receive window; refuses unless the control is enabled and unexpired. Returns receipts."""
    if live_control.decide(control, now) != live_control.SEND:
        raise StreamError("CONTROL_NOT_SENDING")
    receiver = receiver_type(ingestion, activation(env, control), bindings(control))
    # Never outlive the control's expiry, whatever window was requested.
    remaining = (control.expires_at - now).total_seconds()
    receipts = await receiver.run(max_seconds=max(1.0, min(seconds, remaining)), max_events=events)
    return len(receipts)


def main(argv: Sequence[str], env: Mapping[str, str] | None = None) -> int:
    env = os.environ if env is None else env
    parser = argparse.ArgumentParser(prog="zava_forward.api.live_receiver")
    parser.add_argument("--control-file", default=env.get("ZF_SIM_CONTROL_FILE", ""))
    parser.add_argument("--seconds", type=float, default=240.0)
    parser.add_argument("--events", type=int, default=1000)
    args = parser.parse_args(list(argv))
    try:
        if not args.control_file:
            raise StreamError("CONTROL_REQUIRED")
        control = live_control.load(Path(args.control_file))
        from zava_forward.core.factory import open_store

        count = asyncio.run(
            run_window(
                control,
                env,
                SensorIngestion(open_store(env)),
                args.seconds,
                args.events,
                datetime.now(UTC),
            )
        )
    except (StreamError, SystemExit) as error:
        print(f"Cannot run: {error}", file=sys.stderr)
        return 2
    except Exception:  # noqa: BLE001 - fixed code only, never a traceback or connection detail
        print("Cannot run: RECEIVER_FAILED", file=sys.stderr)
        return 4
    print(f"receipts={count}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
