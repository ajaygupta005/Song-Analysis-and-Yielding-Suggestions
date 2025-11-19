"""
Diagnostic script to check Spark/Java environment
"""
import os
import sys
import subprocess

print("=" * 60)
print("SPARK/JAVA ENVIRONMENT DIAGNOSTIC")
print("=" * 60)

# Check Python
print(f"\n✓ Python executable: {sys.executable}")
print(f"✓ Python version: {sys.version}")

# Check JAVA_HOME
java_home = os.environ.get("JAVA_HOME")
print(f"\n{'✓' if java_home else '✗'} JAVA_HOME: {java_home or 'NOT SET'}")

# Check if java is in PATH
try:
    result = subprocess.run(["java", "-version"], capture_output=True, text=True, shell=True)
    java_version = result.stderr.split('\n')[0] if result.stderr else "Unknown"
    print(f"✓ Java version: {java_version}")
except Exception as e:
    print(f"✗ Java not found in PATH: {e}")

# Check HADOOP_HOME
hadoop_home = os.environ.get("HADOOP_HOME")
print(f"\n{'✓' if hadoop_home else '✗'} HADOOP_HOME: {hadoop_home or 'NOT SET'}")

# Check SPARK_HOME
spark_home = os.environ.get("SPARK_HOME")
print(f"{'✓' if spark_home else '○'} SPARK_HOME: {spark_home or 'NOT SET (using bundled PySpark)'}")

# Check PYSPARK_PYTHON
pyspark_python = os.environ.get("PYSPARK_PYTHON")
print(f"\n{'✓' if pyspark_python else '○'} PYSPARK_PYTHON: {pyspark_python or 'NOT SET (will be set by code)'}")

# Try to import PySpark
try:
    import pyspark
    print(f"\n✓ PySpark installed: version {pyspark.__version__}")
    print(f"✓ PySpark location: {pyspark.__file__}")
except ImportError as e:
    print(f"\n✗ PySpark import failed: {e}")

# Check if model exists
model_path = "models/als_model"
if os.path.exists(model_path):
    print(f"\n✓ Model exists at: {model_path}")
else:
    print(f"\n✗ Model not found at: {model_path}")

print("\n" + "=" * 60)
print("RECOMMENDATIONS:")
print("=" * 60)

if not java_home:
    print("⚠ Set JAVA_HOME environment variable to your Java installation")
    print("  Example: JAVA_HOME=C:\\Program Files\\Java\\jdk-11")
    
if not hadoop_home:
    print("⚠ Set HADOOP_HOME for Windows compatibility")
    print("  Example: HADOOP_HOME=C:\\hadoop")

print("\n")
