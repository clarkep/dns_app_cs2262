# The official python base image 
FROM python:3.9-slim

WORKDIR /app

RUN pip install Flask

COPY . .

EXPOSE 9090

CMD ["python", "fib.py"]