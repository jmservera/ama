"""API-owned finite offline composition, deliberately not an HTTP route."""

from zava_forward.core.sensor_consumer import (
    ConsumerError,
    Receipt,
    SensorConsumer,
    preflight,
    utc,
)


class BatchStopped(ConsumerError):
    def __init__(self, error: ConsumerError, completed: tuple[Receipt, ...]) -> None:
        super().__init__(error.code, error.reference)
        self.completed = completed


class SensorIngestion:
    def __init__(self, store: object) -> None:
        self.consumer = SensorConsumer(store)

    def consume(self, observations: object, *, received_at: object) -> tuple[Receipt, ...]:
        batch = preflight(observations)
        if not isinstance(received_at, str):
            raise ConsumerError("INVALID_RECEIPT_TIME")
        try:
            utc(received_at)
        except ValueError:
            raise ConsumerError("INVALID_RECEIPT_TIME") from None
        completed: list[Receipt] = []
        for observation in batch:
            try:
                completed.append(self.consumer.process(observation, received_at))
            except ConsumerError as error:
                raise BatchStopped(error, tuple(completed)) from None
        return tuple(completed)
