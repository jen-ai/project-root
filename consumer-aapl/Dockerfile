FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install pika pymongo
CMD ["python", "consumer.py"]
