"""Event handlers — application-side reactions to domain events.

Add `on_<event>.py` modules per subscription. Handlers depend on
ports just like use cases; they never publish events themselves
(that's the use case's job after it produces the event).
"""
