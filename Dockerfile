# Official Python image
FROM python:3.10-slim

# Set the working directory in container
WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y wget && \
    wget https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64-v0.6.1.tar.gz && \
    tar -C /usr/local/bin -xzvf dockerize-linux-amd64-v0.6.1.tar.gz && \
    rm dockerize-linux-amd64-v0.6.1.tar.gz

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code into the container
COPY . .

RUN python -c "from sentence_transformers import CrossEncoder; CrossEncoder('cross-encoder/ms-marco-MiniLM-L-12-v2')"

# Run the app
CMD ["dockerize", "-wait", "tcp://db:5432", "-timeout", "60s", "python", "gmail_fetch.py"]