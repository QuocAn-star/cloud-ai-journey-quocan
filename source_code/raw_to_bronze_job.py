import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME"])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

job = Job(glueContext)
job.init(args["JOB_NAME"], args)

BUCKET_NAME = "customer-behavior-lakehouse1"

RAW_PATH = f"s3://{BUCKET_NAME}/raw/"
BRONZE_PATH = f"s3://{BUCKET_NAME}/bronze/"

# ==========================
# CSV Tables
# ==========================

csv_tables = [
    "customers",
    "orders",
    "products",
    "order_items",
    "reviews",
    "sessions"
]

for table in csv_tables:

    input_path = f"{RAW_PATH}{table}.csv"
    output_path = f"{BRONZE_PATH}{table}/"

    print(f"Reading CSV: {input_path}")

    df = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(input_path)
    )

    (
        df.write
        .mode("overwrite")
        .parquet(output_path)
    )

    print(f"Saved Bronze: {table}")

# ==========================
# Streaming Events (Firehose)
# ==========================

events_path = f"s3://{BUCKET_NAME}/raw/streaming/events/2026/07/06/08/"

print(f"Reading Streaming Events recursively: {events_path}")

events_df = spark.read.json(events_path)

events_df = (
    spark.read
    .option("recursiveFileLookup", "true")
    .json(events_path)
)

print("Saved Bronze: events")

print("Raw → Bronze completed successfully.")

job.commit()