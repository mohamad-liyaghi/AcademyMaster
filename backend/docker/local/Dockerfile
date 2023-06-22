# Use a lightweight Python 3.11 image
FROM python:3.11-alpine

# Set an environment variable to avoid buffering of the standard output
ENV PYTHONUNBUFFERED=1

# Set the working directory to /backend
WORKDIR /backend

# Upgrade pip to the latest version
RUN pip install --upgrade pip 

RUN ls -a 

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the required Python packages
RUN pip install -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Expose port 8000 to the outside world
EXPOSE 8000