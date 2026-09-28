FROM python:3.13-slim
RUN useradd --create-home app
WORKDIR /app
COPY app/ /app/
USER app
EXPOSE 8000
CMD ["python", "server.py"]
