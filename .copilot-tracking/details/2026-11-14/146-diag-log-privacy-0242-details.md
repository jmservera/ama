# Details

* live_simulator.py StdoutSink.send: label = SYNTHETIC if present in body else UNLABELLED; print DRY-RUN device message label bytes=N.
* Tests use real iot_stream.decode, real StdoutSink and ls.main failure path; redaction installed via core diagnostic_logging.
