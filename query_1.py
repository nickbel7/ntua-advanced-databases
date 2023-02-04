from load_data import *

#### ==== QUERY 1 ====

# Να βρεθεί η διαδρομή με το μεγαλύτερο φιλοδώρημα (tip) τον Μάρτιο και σημείο
# άφιξης το "Battery Park".
# -----------------------------------------------

# === SQL ===
sql_str = \
    "SELECT taxi_trips.* " + \
    "FROM taxi_trips " + \
    "JOIN zone_lookups ON taxi_trips.DOLocationID = zone_lookups.LocationID " + \
    "WHERE zone_lookups.Zone = 'Battery Park' " + \
    "AND MONTH(taxi_trips.tpep_dropoff_datetime) = 3 " + \
    "ORDER BY taxi_trips.tip_amount DESC " + \
    "LIMIT 1;"

# start_time = time.time()
# res = spark.sql(sql_str)
# res.show()

# print('Total time for SQL: ',time.time() - start_time , 'sec')

# -----------------------------------------------

# === DataFrame ===
total_time = 0

for i in range(n_iter): 
    start_time = time.time()

    res = taxi_trips_df.filter(month(col("tpep_pickup_datetime")) == 3)\
        .join(zone_lookups_df, taxi_trips_df.DOLocationID == zone_lookups_df.LocationID, "inner")\
        .filter(col("zone") == 'Battery Park')\
        .orderBy(col("tip_amount").desc())\
        .limit(1)
    
    res.count()
    total_time += time.time() - start_time

res.show()
print('Average Total time for DataFrame: ', str(total_time/n_iter), 'sec')
f.write('Average Time for Q1: ' + str(total_time/n_iter) + '\n')
f.close()
