from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.streaming import  DataStreamReader, StreamingQuery, StreamingQueryManager
from pyspark.sql.functions import explode, col, date_format, current_date
from schema import NvdSchema
from typing import Callable
from functools import partial


class Pipeline(object):

    @classmethod
    def get_spark(cls) -> SparkSession:

        spark: SparkSession = SparkSession \
            .builder \
            .appName("SparkStreamingApp") \
            .master("local[*]")\
            .config("spark.jars.packages",
                    "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.0") \
            .enableHiveSupport()\
            .getOrCreate()

        return spark

    @classmethod
    def read(cls,
             spark: SparkSession,
             path: str) -> DataFrame:

        raw: DataStreamReader = spark.readStream \
            .json(path=path,
                  schema=NvdSchema,
                  mode="FAILFAST")

        raw.printSchema()

        return raw

    @classmethod
    def transform(cls,
                  spark: SparkSession,
                  datastream: DataStreamReader ) -> DataFrame:

        transformed: StreamingQuery = datastream\
            .withColumn("CVE_Item", explode(col("CVE_Items")))\
            .select(col("CVE_Item.*"),
                    date_format(current_date(),
                                "YYYY-mm-dd").alias("dw_date"))

        transformed.printSchema()

        return transformed

    @staticmethod
    def writer(spark: SparkSession,
               df: DataFrame)->Callable[[DataFrame, str], None]:

        def batch_writer( df:DataFrame, epoch_id: str)->None:

            spark.logger.info(epoch_id)

            df\
                .format("orc") \
                .outputMode("overwrite") \
                .partitionBy(["dw_date",]) \
                .saveAsTable("prod.cve_data_by_hour")

        return batch_writer()

    @classmethod
    def write(cls,
              spark: SparkSession,
              query: StreamingQuery) -> StreamingQueryManager:

        query.printSchema()

        query_cts : StreamingQueryManager = query.writeStream\
            .foreachBatch(partial(cls.writer, spark))\
            .start()

        return query_cts

    @classmethod
    def run(cls,
            path: str = "/local/logs/*") -> StreamingQueryManager:

        spark: SparkSession = cls.get_spark()
        read: DataFrame = cls.read(spark, path)
        transformed: DataFrame = cls.transform(spark, read)
        written: StreamingQueryManager = cls.write(spark, transformed)

        return written


def main():

    Pipeline.run()


if __name__ == "__main__":

    main()




