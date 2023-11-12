# Coinbase Market Data Pipeline
A data pipeline involves Apache Kafka, Apache Spark, Apache Airflow and Amazon S3 to ingest, process and store market data from public Coinbase Market API.

## Coinbase Market Data API
[Coinbase Market Data](https://docs.cloud.coinbase.com/exchange/docs/websocket-overview) - Coinbase websocket to market data including level 2 orderbook data.

## Architecture
The pipeline is built using the following components:
- A python script which fetch data from Coinbase Market Data API using websocket protocol and publish data to Kafka cluster as producer
- A Kafka cluster
- A spark cluster and a job running on it to process data
- Amazon S3 bucket to store processed data
- Airflow to orchestrate

```
Pipeline Architecture Diagram

+-------------------+    +--------------+    +--------------+    +---------+
|   Data Ingestor   |    | Apache Kafka |    | Apache Spark |    | Amazon  |
|  (via WebSocket)  | -> | Cluster      | -> | Cluster/Job  | -> | S3      |
|                   |    |              |    |              |    | Bucket  |
+-------------------+    +--------------+    +--------------+    +---------+
                                 |                 |                 |
                                 |                 |                 |
                                 +-----------------+-----------------+
                                            |
                                        +-----------------+
                                        | Apache Airflow  |
                                        +-----------------+

```