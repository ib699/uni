# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory
WORKDIR /usr/src/app

# Copy the Python script and shell script into the container
COPY task.py .
COPY run_task.sh .
COPY /etc/rancher/k3s/k3s.yaml .

# Make the shell script executable
RUN chmod +x run_task.sh

# Install any required Python packages (if necessary)
RUN pip install --no-cache-dir -r requirements.txt

# Run the shell script
CMD ["./run_task.sh"]