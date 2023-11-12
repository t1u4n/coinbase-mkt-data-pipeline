from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
import os
from dotenv import load_dotenv

class DataProcessor:
    """This class is used to process data from Kafka."""
    KAFKA_URLS = os.getenv('KAFKA_URLS')
    S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY')
    S3_SECRET_KEY = os.getenv('S3_SECRET_KEY')
    APP_NAME = 'DataProcessorFromKafkaToS3'

    def __init__(self, topics: str, s3_bucket_path: str, checkpoint_path: str) -> None:
        """Constructor of DataProcessor."""
        self._topics = topics
        self._s3_bucket_path = s3_bucket_path
        self._checkpoint_path = checkpoint_path
        self.spark = SparkSession \
            .builder \
            .appName(self.APP_NAME) \
            .config("spark.hadoop.fs.s3a.access.key", self.S3_ACCESS_KEY) \
            .config("spark.hadoop.fs.s3a.secret.key", self.S3_SECRET_KEY) \
            .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
            .getOrCreate()
        self.spark.sparkContext.setLogLevel("ERROR")
    
    def run(self) -> None:
        """This method is used to run the data processor to process data from Kafka."""
        df = self._get_stream_dataframe()
        transformed_df = self._transform_data(df)
        self._export_data(transformed_df)

    def _get_stream_dataframe(self) -> 'DataFrame':
        """This method is used to get the stream dataframe from Kafka."""
        return self.spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", self.KAFKA_URLS) \
            .option("subscribe", self._topics) \
            .load()

    def _transform_data(self, df: 'DataFrame') -> 'DataFrame':
        """This method is used to transform the data from Kafka."""
        return df.selectExpr("CAST(value AS STRING)")
    
    def _export_data(self, df: 'DataFrame') -> None:
        """This method is used to export the data to the storage system."""
        stream_query = (df.writeStream
                    .format("parquet")
                    .outputMode("append")
                    .option("path", self._s3_bucket_path)
                    .option("checkpointLocation", self._checkpoint_path)
                    .start())
        stream_query.awaitTermination()

if __name__ == '__main__':
    load_dotenv()

    topics = "BTC-USD"
    s3_path = "til/coinbase/mkt-data-bucket"
    checkpoint_location = "spark/checkpoint"
    data_processor = DataProcessor(topics, s3_path, checkpoint_location)
    data_processor.run()