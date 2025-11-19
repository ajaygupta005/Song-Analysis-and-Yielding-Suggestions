# Docker Setup Instructions

## Changes Made

1. **Added Java 11 to Dockerfile** - Required for PySpark to run
2. **Set JAVA_HOME environment variable** - Points to Java installation
3. **Updated entrypoint.sh** - Sets PYSPARK_PYTHON and verifies Java

## Rebuild and Run Docker Container

### Step 1: Stop and Remove Existing Container
```bash
docker-compose down
```

### Step 2: Rebuild the Docker Image
```bash
docker-compose build --no-cache
```

### Step 3: Start the Container
```bash
docker-compose up
```

Or run in detached mode:
```bash
docker-compose up -d
```

### Step 4: View Logs (if running in detached mode)
```bash
docker-compose logs -f
```

### Step 5: Access the Application
Open your browser and go to:
```
http://localhost:8501
```

## Troubleshooting

### Check if Java is installed in container
```bash
docker exec -it spotify_app java -version
```

### Check environment variables
```bash
docker exec -it spotify_app env | grep JAVA
```

### Access container shell
```bash
docker exec -it spotify_app /bin/bash
```

### Check Spark can initialize
```bash
docker exec -it spotify_app python -c "from pyspark.sql import SparkSession; spark = SparkSession.builder.appName('test').getOrCreate(); print('Spark OK')"
```

## What Was Fixed

The original error `Java gateway process exited before sending its port number` occurred because:
- The Docker container didn't have Java installed
- PySpark requires Java (JRE 8 or 11) to run the Spark engine
- The Dockerfile now installs `openjdk-11-jre-headless`

After rebuilding, Spark should initialize correctly and the recommendations feature will work.
