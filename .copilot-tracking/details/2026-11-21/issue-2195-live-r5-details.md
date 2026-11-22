# Issue 2195 r5 details

Phase 1: `_Conn._run` holds an RLock per connection, reads rows inside it and returns a buffered `_Cursor`; `execute` and `executemany` return it directly. Regression test `SharedConnectionThreads` uses a fake driver that errors when statements overlap.
