# ntua-advanced-databases
Term project for the course 'Advanced Databases' during 9th semester at NTUA

## Contributors
1. Elina Syrri ([ElinaSyr](https://github.com/elinasyr))
1. Nick Bellos ([nickbel7](https://github.com/nickbel7))


## 👣 Steps
1. Install Spark + Hadoop (see instructions at [installation](https://github.com/nickbel7/ntua-advanced-databases/tree/master/installation))

2. Get data from https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
    - Execute the `data/download-data.sh` script to get the .parquet files (from January to June)
    - Execute the `data/concat-data.sh` script to concat .parquet files into one
    
3. Import the data into HDFS with `hdfs dfs -put hdfs://<master-ip>:9000/data/<filename>.parquet`

4. Exeute each query with `python query_{1,5}.py`
(Alternatively execute `exec_all.sh` to run all queries)

## ❓Queries
1. Να βρεθεί η διαδρομή με το μεγαλύτερο φιλοδώρημα (tip) τον Μάρτιο και σημείο άφιξης το "Battery Park". 
2. Να βρεθεί, για κάθε μήνα, η διαδρομή με το υψηλότερο ποσό στα διόδια. Αγνοήστε μηδενικά ποσά.
3. Να βρεθεί, ανά 15 ημέρες, ο μέσος όρος της απόστασης και του κόστους για όλες τις διαδρομές με σημείο αναχώρησης διαφορετικό από το σημείο άφιξης.
4. Να βρεθούν οι τρεις μεγαλύτερες (top 3) ώρες αιχμής ανά ημέρα της εβδομάδος, εννοώντας τις ώρες (π.χ., 7-8πμ, 3-4μμ, κλπ) της ημέρας με τον μεγαλύτερο αριθμό επιβατών σε μια κούρσα ταξί. Ο υπολογισμός αφορά όλους τους μήνες.
5. Να βρεθούν οι κορυφαίες πέντε (top 5) ημέρες ανά μήνα στις οποίες οι κούρσες είχαν το μεγαλύτερο ποσοστό σε tip. Για παράδειγμα, εάν η κούρσα κόστισε 10$ (fare_amount) και το tip ήταν 5$, το ποσοστό είναι 50%.

## 🗒️ Notes
#### Our Infrastructure
- 1 Master Node : 10.0.0.1
    - 1 Master (Spark)
    - 1 Worker (Spark)
    - 1 Namenode (HDFS)
    - 1 Datanode (HDFS)
- 1 Worker Node : 10.0.0.2
    - 1 Worker (Spark)
    - 1 Datanode (HDFS)

#### [Spark Configuration Parameters](https://spark.apache.org/docs/latest/configuration.html)

