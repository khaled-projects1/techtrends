# Dockerfile
FROM python:3.8

WORKDIR /app

# Copy files from /techtrends directory into /app directory in container
COPY /techtrends  .
#COPY app.py .
# Install dependencies and initialize database
RUN pip install -r requirements.txt
RUN python init_db.py

# Expose port
EXPOSE 3111

# Command to run the application
CMD ["python", "app.py"]

