# Coinbase Market Data Pipeline
## TL;DR
A data pipeline involves Apache Kafka, Apache Spark, and Amazon S3 to ingest, process and store market data from public Coinbase Market API, orchestrated by docker compose.

## Coinbase Market Data API
[Coinbase Market Data](https://docs.cloud.coinbase.com/exchange/docs/websocket-overview) - Coinbase websocket to market data including level 2 orderbook data.

## Quick Start
To run this project locally, you need to have installed `docker`, `docker-compose` and you also need an AWS account. Please set `S3_ACCESS_KEY` and `S3_SECRET_KEY`
 with appropriate value. And then run following command to start the service.
```
docker-compose up
```

## Architecture
The pipeline is built using the following components, orchestrated by docker compose:
- A python script which fetch data from Coinbase Market Data API using websocket protocol and publish data to Kafka cluster as producer
- A Kafka cluster
- A spark cluster and a job running on it to process data
- Amazon S3 bucket to store processed data

```
Pipeline Architecture Diagram

+-------------------+    +--------------+    +------------------+    +---------+
|   Data Ingestor   |    | Apache Kafka |    | Apache Spark     |    | Amazon  |
|  (via WebSocket)  | -> | Cluster      | -> | Cluster/Job      | -> | S3      |
|                   |    |              |    | (Data Processor) |    | Bucket  |
+-------------------+    +--------------+    +------------------+    +---------+
          |                      |                    |                   |
          |                      |                    |                   |
          +----------------------+--------------------+-------------------+
                                 |
                        +-----------------+
                        | Docker Compose  |
                        +-----------------+

```