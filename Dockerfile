# https://hub.docker.com/_/python
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src/ src/

EXPOSE 8000

CMD ["python", "src/record_dataset.py"]
