# Download taxi-trip data from here: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
# Specifically we download all the files from January to June Year 2022
wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-01.parquet
wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-02.parquet
wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-03.parquet
wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-04.parquet
wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-05.parquet
wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-06.parquet

# Download here: https://d37ci6vzurychx.cloudfront.net/misc/taxi+_zone_lookup.csv
# This csv is the linkage LocationID and Zone/Borough Location 
wget https://d37ci6vzurychx.cloudfront.net/misc/taxi+_zone_lookup.csv
