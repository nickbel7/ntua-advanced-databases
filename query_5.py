from load_data import *

#### ==== QUERY 5 ====

# Να βρεθούν οι κορυφαίες πέντε (top 5) ημέρες ανά μήνα στις οποίες οι κούρσες είχαν το 
# μεγαλύτερο ποσοστό σε tip. Για παράδειγμα, εάν η κούρσα κόστισε 10$ (fare_amount) και 
# το tip ήταν 5$, το ποσοστό είναι 50%.
# -----------------------------------------------

# === SQL ===
sql_str = \
    "WITH taxi_trips_tmp AS " + \
    "(SELECT " + \
    "MONTH(tpep_pickup_datetime) AS pickup_month, " + \
    "DAY(tpep_pickup_datetime) AS pickup_day, " + \
    "AVG((tip_amount / fare_amount) * 100) AS tip_percentage_avg " + \
    "FROM taxi_trips " + \
    "WHERE MONTH(tpep_pickup_datetime) BETWEEN 1 AND 6 " + \
    "GROUP BY pickup_day, pickup_month)" + \
    "SELECT pickup_month, pickup_day, tip_percentage_avg " + \
    "FROM (" + \
    "SELECT " + \
    "pickup_month, " + \
    "pickup_day, " + \
    "tip_percentage_avg, " + \
    "ROW_NUMBER() " + \
    "OVER (PARTITION BY pickup_month ORDER BY tip_percentage_avg DESC) AS row " + \
    "FROM taxi_trips_tmp) " + \
    "WHERE row <= 5 " + \
    "ORDER BY pickup_month, pickup_day;"

# start_time = time.time()

# res = spark.sql(sql_str)

# res.show()
# print('Total time for SQL: ', time.time() - start_time, 'sec')

# -----------------------------------------------

# === DataFrame ===
total_time = 0

for i in range(n_iter):
    start_time = time.time()

    taxi_trips_df_tmp = taxi_trips_df.withColumn("tip_percentage", ((col("tip_amount") / col("fare_amount")) * 100))\
        .groupBy(dayofmonth(col("tpep_pickup_datetime")).alias("pickup_day"), month(col("tpep_pickup_datetime")).alias("pickup_month"))\
        .agg(avg("tip_percentage").alias("tip_percentage_avg"))

    window_month = Window.partitionBy("pickup_month").orderBy(col("tip_percentage_avg").desc())

    res = taxi_trips_df_tmp.select(col("pickup_month"), col("pickup_day"), col("tip_percentage_avg"))\
        .withColumn("row", row_number().over(window_month))\
        .filter(col("row") <= 5)\
        .drop("row")\
        .orderBy(col("pickup_month"), col("pickup_day"))
    
    res.collect()
    total_time += time.time() - start_time

res.show()
print('Average Total time for DataFrame: ', str(total_time/n_iter), 'sec')
f.write('Average Time for Q5: ' + str(total_time/n_iter) + '\n')
f.close()

