"""Domain layer — entities, value objects, ports, domain events.

Importing anything from infrastructure or interfaces from this layer
is a violation of the dependency rule. The domain knows nothing about
its persistence story or its transports.
"""
