FROM python:3.9-slim

# Install cron and ffmpeg
RUN apt-get update && apt-get install -y cron ffmpeg

# Install Python dependencies
RUN pip install requests beautifulsoup4 cloudscraper selenium webdriver-manager

# Set the working directory in the container
WORKDIR /app

# Copy the Python script into the container
COPY src/ .

# Create a directory for downloaded videos
RUN mkdir /app/tv

# Add crontab file in the cron directory
COPY crontab /etc/cron.d/dailymotion-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/dailymotion-cron

# Apply cron job
RUN crontab /etc/cron.d/dailymotion-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run the command on container startup
CMD python main.py && cron && tail -f /var/log/cron.log