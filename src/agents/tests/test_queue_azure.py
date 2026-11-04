import base64
import unittest
import urllib.parse
from xml.sax.saxutils import escape

from zava_forward.core import assistants

from zava_forward.agents.dispatch import TaskMessage
from zava_forward.agents.queue_azure import AzureTaskQueue, QueueError, checked_endpoint

ENDPOINT = "https://zfstore.queue.core.windows.net"


def message() -> TaskMessage:
    limits = assistants.Limits(
        dict(
            ZF_ASSIST_AUTHORITY="op",
            ZF_ASSIST_CALL_ALLOWANCE="10",
            ZF_ASSIST_TOKEN_ALLOWANCE="1000000",
            ZF_ASSIST_EXPIRES="2999-01-01T00:00:00Z",
        )
    )
    task = dict(
        id="t1",
        capability="stock-prioritisation",
        case_id="ZF-1",
        version=assistants.VERSION,
        source_signature="sig",
        fence=3,
        owner="own",
        snapshot={"citations": ["home.epc"], "unknowns": []},
    )
    return TaskMessage.from_task(task, limits)


def entry(text: str, count: int = 1, message_id: str = "m1", pop: str = "p1==") -> bytes:
    return (
        "<QueueMessagesList><QueueMessage>"
        f"<MessageId>{message_id}</MessageId><PopReceipt>{pop}</PopReceipt>"
        f"<DequeueCount>{count}</DequeueCount><MessageText>{escape(text)}</MessageText>"
        "</QueueMessage></QueueMessagesList>"
    ).encode()


class Recorder:
    """Scripted transport: replies are consumed in order and every call is kept."""

    def __init__(self, *replies: tuple[int, bytes]) -> None:
        self.replies = list(replies)
        self.calls: list[tuple[str, str, dict[str, str], bytes | None]] = []

    def __call__(
        self, method: str, url: str, headers: dict[str, str], body: bytes | None
    ) -> tuple[int, bytes]:
        self.calls.append((method, url, headers, body))
        return self.replies.pop(0)


def queue(recorder: Recorder, **kwargs: int) -> AzureTaskQueue:
    return AzureTaskQueue(
        ENDPOINT, "agent-tasks", "agent-tasks-poison", lambda: "fake-token", recorder, **kwargs
    )


class ReceiveTests(unittest.TestCase):
    def test_leases_one_message_with_bearer_token_and_returns_task(self) -> None:
        text = message().to_json()
        rec = Recorder((200, entry(base64.b64encode(text.encode()).decode())))
        received = queue(rec).receive()
        assert received is not None
        receipt, task = received
        self.assertEqual(task.to_json(), text)
        self.assertEqual(receipt, "m1\np1==")
        method, url, headers, _ = rec.calls[0]
        self.assertEqual(method, "GET")
        query = urllib.parse.parse_qs(urllib.parse.urlsplit(url).query)
        self.assertEqual(query["numofmessages"], ["1"])
        self.assertEqual(query["visibilitytimeout"], ["60"])
        self.assertEqual(headers["Authorization"], "Bearer fake-token")

    def test_plain_json_text_is_accepted(self) -> None:
        rec = Recorder((200, entry(message().to_json())))
        self.assertIsNotNone(queue(rec).receive())

    def test_empty_queue_returns_none(self) -> None:
        rec = Recorder((200, b"<QueueMessagesList />"))
        self.assertIsNone(queue(rec).receive())

    def test_malformed_xml_is_a_queue_error(self) -> None:
        with self.assertRaises(QueueError):
            queue(Recorder((200, b"<not-xml"))).receive()

    def test_non_numeric_dequeue_count_is_a_queue_error(self) -> None:
        rec = Recorder((200, entry("x").replace(b"<DequeueCount>1", b"<DequeueCount>abc")))
        with self.assertRaises(QueueError):
            queue(rec).receive()

    def test_service_error_raises_for_the_loop_to_retry(self) -> None:
        with self.assertRaises(QueueError):
            queue(Recorder((503, b""))).receive()

    def test_malformed_message_goes_to_poison_queue_then_is_deleted(self) -> None:
        rec = Recorder((200, entry("not json")), (201, b""), (204, b""))
        self.assertIsNone(queue(rec).receive())
        self.assertEqual([c[0] for c in rec.calls], ["GET", "POST", "DELETE"])
        self.assertIn("agent-tasks-poison/messages", rec.calls[1][1])
        self.assertIn("agent-tasks/messages/m1", rec.calls[2][1])

    def test_repeated_delivery_is_poisoned_without_running(self) -> None:
        rec = Recorder((200, entry(message().to_json(), count=6)), (201, b""), (204, b""))
        self.assertIsNone(queue(rec).receive())
        self.assertEqual(rec.calls[1][0], "POST")

    def test_failed_poison_write_keeps_the_message(self) -> None:
        rec = Recorder((200, entry("garbage")), (500, b""))
        with self.assertRaises(QueueError):
            queue(rec).receive()
        self.assertEqual([c[0] for c in rec.calls], ["GET", "POST"])


class AckReleaseTests(unittest.TestCase):
    def test_ack_deletes_with_pop_receipt(self) -> None:
        rec = Recorder((204, b""))
        queue(rec).ack("m1\np1==")
        method, url, _, _ = rec.calls[0]
        self.assertEqual(method, "DELETE")
        self.assertIn("popreceipt=p1%3D%3D", url)

    def test_release_makes_message_visible_at_once(self) -> None:
        rec = Recorder((204, b""))
        queue(rec).release("m1\np1==")
        method, url, _, _ = rec.calls[0]
        self.assertEqual(method, "PUT")
        self.assertIn("visibilitytimeout=0", url)

    def test_expired_lease_is_not_an_error(self) -> None:
        queue(Recorder((404, b""))).ack("m1\np1==")

    def test_failed_delete_raises(self) -> None:
        with self.assertRaises(QueueError):
            queue(Recorder((500, b""))).ack("m1\np1==")

    def test_malformed_receipt_is_refused(self) -> None:
        with self.assertRaises(ValueError):
            queue(Recorder()).ack("no-separator")


class ConfigurationTests(unittest.TestCase):
    def test_only_plain_https_origins_are_accepted(self) -> None:
        self.assertEqual(checked_endpoint(ENDPOINT + "/"), ENDPOINT)
        for bad in (
            "http://zfstore.queue.core.windows.net",
            "https://user:pw@zfstore.queue.core.windows.net",
            "https://zfstore.queue.core.windows.net/q",
            "https://zfstore.queue.core.windows.net?sig=x",
            "",
        ):
            with self.subTest(endpoint=bad), self.assertRaises(ValueError):
                checked_endpoint(bad)

    def test_queue_names_are_validated(self) -> None:
        with self.assertRaises(ValueError):
            AzureTaskQueue(ENDPOINT, "../x", "poison", lambda: "t", Recorder())


if __name__ == "__main__":
    unittest.main()
