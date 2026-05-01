"""Infrastructure layer — adapters that implement domain ports.

Free to import vendor libraries (SQLAlchemy, pika, requests). Must
not be imported by domain or application; only interfaces/ wires it
together.
"""
