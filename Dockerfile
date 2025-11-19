FROM python:3.10-slim

# Prevent interactive prompts during install
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies including Java 21 for PySpark
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        wget \
        curl \
        git \
        openjdk-21-jre-headless \
    && rm -rf /var/lib/apt/lists/*

# Set Java environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Create app directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entrypoint script and the rest of the project
COPY . .

# Make the entrypoint script executable
RUN chmod +x ./docker/entrypoint.sh

# Expose Streamlit port
EXPOSE 8501

# Set the ENTRYPOINT to the script that launches Streamlit
ENTRYPOINT ["./docker/entrypoint.sh"]
CMD []