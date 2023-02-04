from load_data import *
#### ==== QUERY 3 ====

# Να βρεθεί, ανά 15 ημέρες, ο μέσος όρος της απόστασης και του κόστους για όλες τις
# διαδρομές με σημείο αναχώρησης διαφορετικό από το σημείο άφιξης.
# -----------------------------------------------

# === SQL ===
sql_str = \
    "WITH taxi_trips_tmp AS" + \
        "(SELECT tpep_pickup_datetime, PULocationID, DOLocationID, trip_distance, total_amount, " + \
        "CASE " + \
        "WHEN DAY(tpep_pickup_datetime) <= 15 THEN " + \
        "CONCAT(MONTH(tpep_pickup_datetime), '-a') " + \
        "ELSE " + \
        "CONCAT(MONTH(tpep_pickup_datetime), '-b') " + \
        "END AS month_half " + \
        "FROM taxi_trips) " + \
    "SELECT month_half, " + \
        "AVG(trip_distance) AS avg_trip_distance, " + \
        "AVG(total_amount) AS avg_total_amount " + \
    "FROM taxi_trips_tmp " + \
    "WHERE PULocationID != DOLocationID " + \
    "GROUP BY month_half " + \
    "ORDER BY month_half ASC; " 

# start_time = time.time()

# res = spark.sql(sql_str)

# res.show()

# print('Total time for SQL: ', time.time() - start_time, 'sec')

# -----------------------------------------------

# === DataFrame ===
total_time = 0

for i in range(n_iter):
    start_time = time.time()

    taxi_trips_df_tmp = taxi_trips_df.withColumn("month_half",\
        expr("case when day(tpep_pickup_datetime) <= 15 \
            then concat(month(tpep_pickup_datetime),'-a') \
            else concat(month(tpep_pickup_datetime),'-b') end"))

    res = taxi_trips_df_tmp.filter(col("PULocationID") != col("DOLocationID"))\
        .groupBy("month_half")\
        .agg(avg("trip_distance"), avg("total_amount"))\
        .orderBy(asc("month_half"))
    
    res.count()
    total_time += time.time() - start_time

res.show()
print('Average Total time for DataFrame: ', str(total_time/n_iter), 'sec')
# f.write('Average Time for Q3: ' + str(total_time/n_iter) + '\n')


# === RDD ===
total_time = 0
n_iter = 5

for i in range(n_iter):
    start_time = time.time()

    final_rdd = taxi_trips_rdd.filter(lambda x: x.PULocationID != x.DOLocationID)\
        .map(lambda x: (f"{x.tpep_pickup_datetime.month}-{'a' if x.tpep_pickup_datetime.day <= 15 else 'b'}", (x.trip_distance, x.total_amount, 1)))\
        .reduceByKey(lambda x1,x2: (x1[0]+x2[0], x1[1]+x2[1], x1[2]+x2[2]))\
        .mapValues(lambda x: (x[0]/x[2], x[1]/x[2]))\
        .sortByKey()

    total_time += time.time() - start_time

for x in final_rdd.collect():
    print(x)   
    
print('Average Total time for RDD: ', str(total_time/n_iter), 'sec')
f.write('Average Time for Q3-RDD: ' + str(total_time/n_iter) + '\n')
f.close()
