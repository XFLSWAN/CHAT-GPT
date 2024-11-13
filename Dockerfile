# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV API_ID=""
ENV API_HASH=""
ENV BOT_TOKEN=""
ENV SESSION_NAME=""

# Install system dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the bot code into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the bot
CMD ["python", "bot.py"]
