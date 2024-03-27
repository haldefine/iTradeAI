# https://hub.docker.com/_/python
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

CMD ["python", "./record_dataset.py"]
