from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.streaming import  DataStreamReader, StreamingQuery, StreamingQueryManager
from pyspark.sql.functions import explode, col, date_format, current_date
from .schema import NvdSchema


class Pipeline(object):

    @classmethod
    def get_spark(cls) -> SparkSession:

        spark: SparkSession = SparkSession \
            .builder \
            .appName("SparkStreamingApp") \
            .master("local[*]")\
            .config("spark.jars.packages",
                    "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.0") \
            .getOrCreate()

        return spark

    @classmethod
    def read(cls,
             spark: SparkSession,
             path: str) -> DataFrame:

        raw: DataStreamReader = spark.readStream \
            .format("json")\
            .option("schema", NvdSchema)\
            .option("mode", "FAILFAST")\
            .load(path)

        return raw

    @classmethod
    def transform(cls,
                  spark: SparkSession,
                  datastream: DataStreamReader ) -> DataFrame:

        transformed: StreamingQuery = datastream\
            .withColumn("CVE_Item", explode(col("CVE_Items")))\
            .select(col("CVE_Item.*"))

        transformed.printSchema()

        return transformed

    @classmethod
    def write(cls,
              spark: SparkSession,
              query: StreamingQuery) -> StreamingQueryManager:

        query.start()

        query\
            .writeStream\
            .format("orc")\
            .partitionBy(date_format(col(current_date()), "YYYY-mm-dd"))\
            .saveAsTable("prod.cve_data_by_hour")

        return query

    @classmethod
    def run(cls,
            path: str = "/local/logs/*") -> DataFrame:

        spark: SparkSession = cls.get_spark()
        read: DataFrame = cls.read(spark, path)
        transformed: DataFrame = cls.transform(spark,read)
        written: StreamingQueryManager = cls.write(spark, transformed)

        return written


def main():

    Pipeline.run()


if __name__ == "__main__":

    main()




