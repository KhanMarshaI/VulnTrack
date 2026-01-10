# base image
FROM python:3.10-slim

# working dir
WORKDIR /app

# dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy code from our dir to container working dir
COPY . .

# flask port
EXPOSE 5000

# run app
CMD ["python", "app.py"]