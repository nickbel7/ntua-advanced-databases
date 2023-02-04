# This file concatenates 6 .parquet files into a single .parquet file and saves it
# For this work we utilize a Spark session for the process

from pyspark.sql import SparkSession
import os 
import shutil
import glob 

# create a Spark session
spark = SparkSession.builder.appName("ParquetConcatenation").getOrCreate()

# Concat .parquet files (from month 1 to 6)
df = spark.read.parquet("yellow_tripdata_2022-01.parquet")
for i in range(2, 7):
    df = df.union(spark.read.parquet("yellow_tripdata_2022-0{}.parquet".format(i)))

# Output as one file inside a .parquet folder
df.coalesce(1).write.format("parquet").mode("append").save("temp.parquet")

# Extract the .parquet file from the folder and delete the folder
files = glob.glob("./temp.parquet/*.parquet")
shutil.move(files[0], "yellow_tripdata_2022-01_06.parquet")
shutil.rmtree("./temp.parquet")

# stop the Spark session
spark.stop()
