# getting base python image
FROM python:3.9

# creating working directory and installing requirements 
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copying files into working directory
COPY . .

# running database migrations and then kafka producer and consumer in background
RUN flask db migrate

# define a placeholder command
CMD ["echo", "Placeholder command"]