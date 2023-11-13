#!/bin/bash

# Include Kafka connector
/opt/bitnami/spark/bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1 --master local[2] data_processor.py
