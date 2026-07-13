import sys
import boto3
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql.functions import col, count, countDistinct, sum, avg, to_date, lit
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME"])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

job = Job(glueContext)
job.init(args["JOB_NAME"], args)

BUCKET_NAME = "customer-behavior-lakehouse1"
DATABASE_NAME = "customer_behavior_catalog_db"

SILVER_PATH = f"s3://{BUCKET_NAME}/silver/"
GOLD_PATH = f"s3://{BUCKET_NAME}/gold/"

glue = boto3.client("glue")


def spark_type_to_athena_type(data_type):
    t = data_type.simpleString()

    if t in ["string"]:
        return "string"
    if t in ["int", "integer"]:
        return "int"
    if t in ["bigint", "long"]:
        return "bigint"
    if t in ["double", "float"]:
        return "double"
    if t in ["date"]:
        return "date"
    if t.startswith("timestamp"):
        return "timestamp"

    return "string"


def register_table(table_name, df, s3_location):
    columns = []

    for field in df.schema.fields:
        columns.append({
            "Name": field.name,
            "Type": spark_type_to_athena_type(field.dataType)
        })

    try:
        glue.delete_table(
            DatabaseName=DATABASE_NAME,
            Name=table_name
        )
        print(f"Deleted old table: {table_name}")
    except glue.exceptions.EntityNotFoundException:
        pass

    glue.create_table(
        DatabaseName=DATABASE_NAME,
        TableInput={
            "Name": table_name,
            "TableType": "EXTERNAL_TABLE",
            "Parameters": {
                "classification": "parquet",
                "EXTERNAL": "TRUE"
            },
            "StorageDescriptor": {
                "Columns": columns,
                "Location": s3_location,
                "InputFormat": "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat",
                "OutputFormat": "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat",
                "SerdeInfo": {
                    "SerializationLibrary": "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe",
                    "Parameters": {
                        "serialization.format": "1"
                    }
                }
            }
        }
    )

    print(f"Registered Glue Catalog table: {table_name}")


def write_gold_table(table_name, df):
    output_path = f"{GOLD_PATH}{table_name}/"

    df.write.mode("overwrite").parquet(output_path)

    register_table(
        table_name=table_name,
        df=df,
        s3_location=output_path
    )


events = spark.read.parquet(f"{SILVER_PATH}events/")
orders = spark.read.parquet(f"{SILVER_PATH}orders/")

orders = orders.withColumn("order_date", to_date(col("order_time")))

event_col = "event_type" if "event_type" in events.columns else "event"

event_summary = (
    events.groupBy(event_col)
    .agg(count("*").alias("total_events"))
    .withColumnRenamed(event_col, "event_type")
)

daily_revenue = (
    orders.groupBy("order_date")
    .agg(sum("total_usd").alias("total_revenue"))
)

payment_summary = (
    orders.groupBy("payment_method")
    .agg(
        count("order_id").alias("total_orders"),
        sum("total_usd").alias("total_revenue"),
        avg("total_usd").alias("avg_order_value")
    )
)

country_revenue = (
    orders.groupBy("country")
    .agg(
        count("order_id").alias("total_orders"),
        sum("total_usd").alias("total_revenue"),
        avg("total_usd").alias("avg_order_value")
    )
)

device_summary = (
    orders.groupBy("device")
    .agg(
        count("order_id").alias("total_orders"),
        sum("total_usd").alias("total_revenue"),
        avg("total_usd").alias("avg_order_value")
    )
)

source_summary = (
    orders.groupBy("source")
    .agg(
        count("order_id").alias("total_orders"),
        sum("total_usd").alias("total_revenue"),
        avg("total_usd").alias("avg_order_value")
    )
)

total_events = events.count()

dashboard_summary = (
    orders.agg(
        countDistinct("order_id").alias("total_orders"),
        countDistinct("customer_id").alias("total_customers"),
        sum("total_usd").alias("total_revenue"),
        avg("total_usd").alias("avg_order_value")
    )
    .withColumn("total_events", lit(total_events))
)

write_gold_table("event_summary", event_summary)
write_gold_table("daily_revenue", daily_revenue)
write_gold_table("payment_summary", payment_summary)
write_gold_table("country_revenue", country_revenue)
write_gold_table("device_summary", device_summary)
write_gold_table("source_summary", source_summary)
write_gold_table("dashboard_summary", dashboard_summary)

print("Silver to Gold job completed and Glue Catalog tables registered.")

job.commit()