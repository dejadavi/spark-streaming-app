from setuptools import setup, find_packages

setup(
    name="spark-app",
    version="0.1",
    packages=find_packages(),
    package_dir={
        "": ".",
    },
)