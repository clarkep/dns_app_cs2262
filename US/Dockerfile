# The official python base image 
FROM python:3.9-slim

WORKDIR /app

RUN pip install Flask

COPY . .

EXPOSE 8080

CMD ["python", "app.py"]
