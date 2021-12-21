from setuptools import setup, find_packages

setup(
    name="spark_app",
    version="0.1",
    packages=find_packages(),
    package_dir={
        "spark_app": ".",
    },
    requires=[
        "pyspark",
        "pandas",
        "build",
        "mypy",
        "Click",
        "pyarrow"
    ],
    entry_points='''
        [console_scripts]
        spark-app=cli:cli
    ''',
)