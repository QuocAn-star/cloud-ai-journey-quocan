import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql.functions import col, trim, to_timestamp
from pyspark.sql.types import StringType
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME"])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

job = Job(glueContext)
job.init(args["JOB_NAME"], args)

BUCKET_NAME = "customer-behavior-lakehouse1"

BRONZE_PATH = f"s3://{BUCKET_NAME}/bronze/"
SILVER_PATH = f"s3://{BUCKET_NAME}/silver/"

tables = [
    "customers",
    "orders",
    "products",
    "order_items",
    "reviews",
    "sessions",
    "events"
]


def clean_column_name(name):
    return (
        name.strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
    )


for table in tables:
    input_path = f"{BRONZE_PATH}{table}/"
    output_path = f"{SILVER_PATH}{table}/"

    print(f"Reading Bronze: {input_path}")

    df = spark.read.parquet(input_path)

    df = df.dropDuplicates()

    for old_col in df.columns:
        new_col = clean_column_name(old_col)
        if old_col != new_col:
            df = df.withColumnRenamed(old_col, new_col)

    for field in df.schema.fields:
        if isinstance(field.dataType, StringType):
            df = df.withColumn(field.name, trim(col(field.name)))

    for column_name in df.columns:
        lower_name = column_name.lower()
        if "date" in lower_name or "time" in lower_name or "timestamp" in lower_name:
            df = df.withColumn(column_name, to_timestamp(col(column_name)))

    print(f"Writing Silver: {output_path}")

    (
        df.write
        .mode("overwrite")
        .parquet(output_path)
    )

print("Bronze to Silver job completed successfully.")

job.commit()