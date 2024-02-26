# Use the official Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the DNS server code into the container
COPY . /app

# Install the required dependencies
RUN pip install Flask

# Expose the DNS server port
EXPOSE 53533/udp

# Run the DNS server
CMD ["python", "dns.py"]
