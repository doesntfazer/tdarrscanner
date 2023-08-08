# Use the Python 3.10 base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy local code to the container image
COPY tdarrscan.py ./tdarrscan.py

# Install necessary packages, Chrome, ChromeDriver, and Python dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends wget unzip && \
    wget https://www.slimjet.com/chrome/download-chrome.php?file=files%2F103.0.5060.53%2Fgoogle-chrome-stable_current_amd64.deb -O google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    wget https://chromedriver.storage.googleapis.com/103.0.5060.134/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    chmod +x chromedriver && \
    mv chromedriver /usr/local/bin/ && \
    rm chromedriver_linux64.zip && \
    pip install --no-cache-dir flask selenium && \
    rm -rf /var/lib/apt/lists/*

# Command to run the application
CMD ["python", "/app/tdarrscan.py"]

