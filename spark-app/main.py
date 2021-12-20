from pyspark.sql import SparkSession

spark: SparkSession  = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spar.jars.config", "some-value") \
    .getOrCreate()