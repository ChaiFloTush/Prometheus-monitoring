FROM python:3-alpine

WORKDIR /app

RUN pip install prometheus-client

COPY prometheus_server.py .

EXPOSE 8080

CMD ["python", "prometheus_server.py"]