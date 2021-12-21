import logging
from logging import Logger
from functools import partial

from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.streaming import  DataStreamReader, StreamingQuery, StreamingQueryManager
from pyspark.sql.functions import explode, col, date_format, current_date

from schema import NvdSchema
from settings import SPARK_PACKAGES


LOGGER: Logger = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


class Job(object):

    @classmethod
    def get_spark(cls) -> SparkSession:

        spark: SparkSession = SparkSession \
            .builder \
            .appName("SparkStreamingApp") \
            .master("local[*]") \
            .config("spark.sql.hive.metastore.jar", "maven") \
            .config("spark.local.dir", "/tmp/spark-temp")\
            .config("spark.sql.sources.partitionOverwriteMode", "dynamic")\
            .config("spark.sql.warehouse.dir","/tmp/spark-warehouse")\
            .config("spark.jars.packages",SPARK_PACKAGES) \
            .enableHiveSupport()\
            .getOrCreate()

        return spark

    @classmethod
    def read(cls,
             spark: SparkSession,
             in_path: str) -> DataFrame:

        raw: DataStreamReader = spark.readStream \
            .format("json")\
            .schema(NvdSchema)\
            .option("mode","FAILFAST") \
            .option("multiline", True)\
            .load(path=in_path)

        raw.printSchema()

        return raw

    @classmethod
    def transform(cls,
                  spark: SparkSession,
                  datastream: DataStreamReader ) -> StreamingQuery:

        transformed: StreamingQuery = datastream\
            .withColumn("CVE_Item", explode(col("CVE_Items")))\
            .select(col("CVE_Item.*"),
                    date_format(current_date(),"yyyy-MM-dd").alias("dw_date"))

        transformed.printSchema()

        return transformed

    @staticmethod
    def writer(spark: SparkSession, df: DataFrame, epoch_id: str) -> None:

        LOGGER.info(epoch_id)

        df\
            .coalesce(1)\
            .write \
            .mode("overwrite") \
            .format("orc")\
            .partitionBy(["dw_date",]) \
            .saveAsTable("cve_data_by_hour")

    @classmethod
    def write(cls,
              spark: SparkSession,
              query: StreamingQuery) -> StreamingQueryManager:

        query.printSchema()

        query_cts : StreamingQueryManager = query.writeStream \
            .trigger(processingTime='30 seconds') \
            .option("checkpointLocation", "/tmp/raw/spark_app/")\
            .foreachBatch(partial(cls.writer, spark))\
            .start()

        return query_cts

    @classmethod
    def run(cls, in_path: str) -> None:

        # Get the sparkSession
        spark: SparkSession = cls.get_spark()

        # Read in the raw data
        raw_df: DataFrame = cls.read(spark, in_path)
        transform_query: StreamingQuery = cls.transform(spark, raw_df)

        # Start the streaming query and await termination(this will run forever as-is)
        query: StreamingQueryManager = cls.write(spark, transform_query)
        query.awaitTermination()

