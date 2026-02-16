# Use the official Python image as the base image
FROM python:3.14

EXPOSE 80/tcp
EXPOSE 8080 

# Create a non-root user and group
# 'useradd' options may vary slightly by Linux distribution (e.g., Alpine uses 'adduser -D')
RUN groupadd --gid 1000 appgroup && useradd --uid 1000 --gid appgroup -m appuser

# Change ownership of application directory to the new user
RUN mkdir /usr/app && chown -R appuser:appgroup /usr/app

# Switch to the non-root user for all subsequent instructions
USER appuser

# Set the working directory in the container
WORKDIR /usr/app

# Copy the requirements file into the container at /app
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Define the command to run the bot when the container starts
CMD ["python", "Bot.py"]
