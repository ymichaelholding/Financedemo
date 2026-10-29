import os
import sys
import pyspark

print("Python:", sys.version)
print("PySpark version:", pyspark.__version__)
print("PySpark location:", pyspark.__file__)

for name in [
    "JAVA_HOME",
    "SPARK_HOME",
    "SPARK_CONF_DIR",
    "PYSPARK_SUBMIT_ARGS",
]:
    print(f"{name}: {os.environ.get(name)}")