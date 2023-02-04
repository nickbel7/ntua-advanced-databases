from load_data import *
from pyspark.sql.functions import rank, dense_rank, row_number
#### ==== QUERY 2 ====

# Να βρεθεί, για κάθε μήνα, η διαδρομή με το υψηλότερο ποσό στα διόδια. Αγνοήστε
# μηδενικά ποσά.
# -----------------------------------------------

# === SQL ===
sql_str = \
"WITH ranked_trips AS ( " + \
"  SELECT *, " + \
"  ROW_NUMBER() " + \
"  OVER (PARTITION BY MONTH(tpep_pickup_datetime) ORDER BY tolls_amount DESC) AS rank " + \
"  FROM taxi_trips " + \
"  WHERE tolls_amount > 0 " + \
") " + \
"SELECT * " + \
"FROM ranked_trips " + \
"WHERE rank = 1 " + \
"ORDER BY MONTH(tpep_pickup_datetime);"

# start_time = time.time()
# res = spark.sql(sql_str)

# res.show()

# print('Total time for SQL: ', time.time() - start_time, 'sec')

# -----------------------------------------------

# === DataFrame ===
total_time = 0

for i in range(n_iter):
    start_time = time.time()

    window = Window.partitionBy(month(col("tpep_pickup_datetime"))).orderBy(col("tolls_amount").desc())

    res = taxi_trips_df.filter(col("tolls_amount") > 0)\
    .withColumn("rank", row_number().over(window))\
    .filter(col("rank") == 1)\
    .orderBy(month(col("tpep_pickup_datetime")).asc())\
    .drop("rank")

    res.count()
    total_time += time.time() - start_time

res.show()
print('Average time for DataFrame: ', str(total_time/n_iter), 'sec')
f.write('Average Time for Q2: ' + str(total_time/n_iter) + '\n')
f.close()
