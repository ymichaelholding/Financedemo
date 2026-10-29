
from setuptools import setup, find_packages

setup(
    name="fiancedemo-etl",
    version="0.1.0",
    description="PySpark ETL framework",
    packages=find_packages(),
    py_modules=["app"],
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "fiancedemo-etl=app:main",
        ],
    },
)
