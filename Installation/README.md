# Installation

### Install Spark
---

[Spark_Install_instructions.pdf](https://github.com/nickbel7/ntua-advanced-databases/blob/master/Installation/Spark_Install_instructions.pdf)


### Install Hadoop

---

[Install-Hadoop](https://sparkbyexamples.com/hadoop/apache-hadoop-installation/)

1. Setup Passwordless Login Between NameNode and DataNode
    
    ```bash
    sudo apt-get update
    sudo apt-get install ssh
    ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
    cat .ssh/id_rsa.pub >> ~/.ssh/authorized_keys
    scp .ssh/authorized_keys worker-node:/home/user/.ssh/authorized_keys
    # Do the same for the worker
    # scp .ssh/authorized_keys master-node:/home/user/.ssh/authorized_keys
    ```
    
    ```
    sudo vi /etc/hosts
    10.0.0.1 master-node
    10.0.0.2 worker-node
    ```
    
2. Download [Hadoop (v.2.7.7)](https://archive.apache.org/dist/hadoop/core/hadoop-2.7.7/) from repository
    
    ```bash
    wget https://archive.apache.org/dist/hadoop/core/hadoop-2.7.7/hadoop-2.7.7.tar.gz
    ```
    
    ```bash
    tar -xzf hadoop-2.7.7.tar.gz
    ```
    
3. Setup environment variables for Hadoop
    
    ```bash
    vi ~/.bashrc
    export HADOOP_HOME=/home/user/hadoop-2.7.7
    export PATH=$PATH:$HADOOP_HOME/bin
    export PATH=$PATH:$HADOOP_HOME/sbin
    export HADOOP_MAPRED_HOME=${HADOOP_HOME}
    export HADOOP_COMMON_HOME=${HADOOP_HOME}
    export HADOOP_HDFS_HOME=${HADOOP_HOME}
    export YARN_HOME=${HADOOP_HOME}
    source ~/.bashrc
    ```
    
4. Update hadoop-env.sh
    
    ```bash
    vi ~/hadoop-2.7.7/etc/hadoop/hadoop-env.sh
    export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
    ```
    
5. Update core-site.xml
`vi ~/hadoop-2.7.7/etc/hadoop/core-site.xml`
    
    ```
    <configuration>
        <property>
            <name>fs.defaultFS</name>
            <value>hdfs://10.0.0.1:9000</value>
        </property>
    </configuration>
    ```
    
6. Update hdfs-site.xml
    
    `vi ~/hadoop-2.7.7/etc/hadoop/hdfs-site.xml`
    
    ```bash
    <configuration>
        <property>
            <name>dfs.replication</name>
            <value>2</value>
        </property>
        <property>
            <name>dfs.namenode.name.dir</name>
            <value>file:///usr/local/hadoop/hdfs/data-namenode</value>
        </property>
        <property>
            <name>dfs.datanode.data.dir</name>
            <value>file:///usr/local/hadoop/hdfs/data-datanode</value>
        </property>
    </configuration>
    ```
    
7. Create data folders (hdfs data)
    
    ```bash
    sudo mkdir -p /usr/local/hadoop/hdfs/data-namenode
    sudo chown user:user -R /usr/local/hadoop/hdfs/data-namenode
    chmod 700 /usr/local/hadoop/hdfs/data-namenode
    ```
    
    ```bash
    sudo mkdir -p /usr/local/hadoop/hdfs/data-datanode
    sudo chown user:user -R /usr/local/hadoop/hdfs/data-datanode
    chmod 700 /usr/local/hadoop/hdfs/data-datanode
    ```
    
8. Create files for MASTER & WORKERS IPs (with the IP of the namenode)
    
    `vi ~/hadoop-2.7.7/etc/hadoop/masters`
    
    ```
    10.0.0.1
    ```
    
    `vi ~/hadoop-2.7.7/etc/hadoop/slaves`
    
    ```
    10.0.0.1
    10.0.0.2
    ```
    
9. Start HDFS cluster
    
    `hdfs namenode -format`
    
    `start-dfs.sh`
    
    Run `jps` to get what processes are running
    
    - What we expect on MASTER
        
        Master
        Worker
        Worker
        NameNode
        DataNode
        SecondaryNameNode
        Jps
        
    - What we expect on WORKER
        
        Worker
        Worker
        DataNode
        Jps
        
    
    📌 Access HDFS UI from : http://<global-ip>:50070
    
    📌 See cluster available datanodes with `hdfs dfsadmin -report`
    
10. (Stop HDFS cluster)
    
    `stop-dfs.sh`
    

### Troobleshooting
---

📌 Διάβαζε πάντα τα logs στο /hadoop-2.7.7/logs

📌 Οι φάκελοι /usr/local/hadoop/hdfs/data-namenode & data-datanode πρέπει να περιέχουν το ίδιο Cluster ID, γιαυτό κάθε φορά τους κάνουμε format (σβήνουμε τα περιεχόμενά τους) και στο Master και στο Worker

📌 Κάνουμε κάθε φορά format τον namenode με `hdfs namenode -format`

### Insert files on HDFS

---

`hdfs dfs -put <filename>.parquet`
