from load_data import *

#### ==== QUERY 4 ====

# Να βρεθούν οι τρεις μεγαλύτερες (top 3) ώρες αιχμής ανά ημέρα της εβδομάδος,
# εννοώντας τις ώρες (π.χ., 7-8πμ, 3-4μμ, κλπ) της ημέρας με τον μεγαλύτερο αριθμό
# επιβατών σε μια κούρσα ταξί (μέσος όρος επιβατών ανά κούρσα). Ο υπολογισμός αφορά όλους τους μήνες.
# -----------------------------------------------

# === SQL ===
sql_str = \
    "WITH avg_passenger_count AS " + \
    "(SELECT DAYOFWEEK(tpep_pickup_datetime) AS pickup_day, " + \
        "HOUR(tpep_pickup_datetime) AS pickup_hour, " + \
        "AVG(passenger_count) AS avg_passenger_count " + \
    "FROM taxi_trips " + \
    "GROUP BY pickup_day, pickup_hour) " + \
    "SELECT pickup_day, " + \
       "pickup_hour, " + \
       "avg_passenger_count " + \
    "FROM " + \
    "(SELECT pickup_day, " + \
        "pickup_hour, " + \
        "avg_passenger_count, " + \
        "ROW_NUMBER() OVER (PARTITION BY pickup_day ORDER BY avg_passenger_count DESC) AS rank " + \
    "FROM avg_passenger_count) " + \
    "WHERE rank <= 3 " + \
    "ORDER BY pickup_day, pickup_hour;"

# start_time = time.time()

# res = spark.sql(sql_str)

# res.show()
# print('Total time for SQL: ', time.time() - start_time, 'sec')

# -----------------------------------------------

# === DataFrame ===
total_time = 0 

for i in range(n_iter):
    start_time = time.time()

    window = Window.partitionBy("pickup_day").orderBy(col("avg_passenger_count").desc())

    res = taxi_trips_df.groupBy(dayofweek(col("tpep_pickup_datetime")).alias("pickup_day"), hour(col("tpep_pickup_datetime")).alias("pickup_hour"))\
        .agg(avg("passenger_count").alias("avg_passenger_count"))\
        .withColumn("rank", row_number().over(window))\
        .filter(col("rank") <= 3)\
        .drop("rank")\
        .orderBy(col("pickup_day").asc(), col("pickup_hour").asc())\

    res.count()
    total_time += time.time() - start_time

res.show(21)
print('Average time for DataFrame: ', str(total_time/n_iter), 'sec')
f.write('Average Time for Q4: ' + str(total_time/n_iter) + '\n')
f.close()

