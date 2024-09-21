# Official Python image
FROM python:3.10-slim

# Set the working directory in container
WORKDIR /usr/src/app

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code into the container
COPY . .

# Run the app
CMD [ "python", "./app.py" ]