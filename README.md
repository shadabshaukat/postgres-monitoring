# Postgres Monitoring Dashboard
A Real-Time Monitoring Dashboard for PostgreSQL 

![Screenshot 2025-02-05 at 14 59 49](https://github.com/user-attachments/assets/857c4ab7-d3db-42da-bdfd-d417fb4b56bb)

![Screenshot 2025-02-05 at 14 59 59](https://github.com/user-attachments/assets/7e77faaa-dfbb-4a5f-a312-95249beda37b)

# Deployment Guide: PostgreSQL Monitoring Dashboard with FastAPI and Docker

Step-by-step instructions to deploy a PostgreSQL monitoring dashboard using FastAPI, Docker, and pg_stat_statements. The dashboard allows you to monitor the performance of multiple PostgreSQL databases and visualize key metrics.

# Table of Contents

   1. Prerequisites

   2. Setup PostgreSQL

   3. Build and Deploy the FastAPI Application
   
   4. Build and Run the Docker Container for the FAST API Application

   5. Access the Dashboard

   6. Troubleshooting

   7. Appendix: SQL Queries

## 1. Prerequisites

Before starting, ensure the following are installed:

    Docker: Install Docker

    Docker Compose: Install Docker Compose

    PostgreSQL 14+: Ensure PostgreSQL is running and accessible.

    Python 3.9+: Required for local testing (optional).

## 2. Setup PostgreSQL

Enable pg_stat_statements

    Edit the PostgreSQL configuration file (postgresql.conf):

```
shared_preload_libraries = 'pg_stat_statements'
pg_stat_statements.max = 10000
pg_stat_statements.track = all
```

Restart the PostgreSQL service:

```
sudo systemctl restart postgresql
```

Create the pg_stat_statements extension in your database:

```
CREATE EXTENSION pg_stat_statements;
```

Depending on your Cloud Platform, the method of addition of PostgreSQL extensions can be different than Self-hosted PostgreSQL.

```
OCI    :  https://docs.oracle.com/en-us/iaas/Content/postgresql/config-list-enable-extension.htm

AWS    :  https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Appendix.PostgreSQL.CommonDBATasks.Extensions.html

Azure  :  https://learn.microsoft.com/en-us/azure/postgresql/extensions/how-to-allow-extensions?tabs=allow-extensions-portal%2Cload-libraries-portal

GCP    :  https://cloud.google.com/sql/docs/postgres/extensions
```

## 3. Build and Deploy the FastAPI Application

Clone the repository containing the FastAPI application:

```
git clone https://github.com/shadabshaukat/postgres-monitoring.git && cd postgres-monitoring
```

Set Up Environment Variables

```
export DATABASES='{"prod_db":"postgresql://postgres:YOurPassword1234%23%5F@10.180.2.171:5432/postgres","stage_db":"postgresql://postgres:YOurPassword1234%23%5F@10.180.2.228:5432/dvdrental"}'
```

Replace the connection strings with your actual database credentials. URL-encode special characters in passwords (e.g., # → %23, _ → %5F). Ref : https://www.w3schools.com/tags/ref_urlencode.ASP 

Alternately you can use a .env file in your docker container. First create a .env file

```
echo 'DATABASES={"prod_db":"postgresql://postgres:YOurPassword1234%23%5F@10.180.2.171:5432/postgres","stage_db":"postgresql://postgres:YOurPassword1234%23%5F@10.180.2.228:5432/dvdrental"}' > .env
```

Ensure the .env file is correctly referenced in the docker-compose.yml file:
```
services:
  monitoring:
    build: .
    env_file: .env
    ports:
      - "8000:8000"
```

## 4. Build and Run the Docker Container for the FAST API Application

Build the Docker image:
```
docker-compose build
```

Start the container:
```
docker-compose up -d
```

Verify the Deployment:
```
docker-compose logs -f
```

Verify the container is running:
```
docker container ls
```

Stop the Container:
```
docker-compose stop
```

Stop and Remove the Container:
```
docker-compose down
```


## 5. Access the Dashboard

Open your browser and navigate to:
```
http://localhost:8000
```

Use the dropdown to select a database and view performance metrics.


## 6. Troubleshooting

Common Issues

    Port Not Bound:

        Ensure the container is running:
       
        docker container ls
       

        Check the logs for errors
       
        docker-compose logs -f
        

Database Connection Errors:

        Verify the connection strings in the .env file.

        Test the connection strings manually using psql.

        psql "postgresql://postgres:YOurPassword1234%23%5F@10.180.2.171:5432/postgres"

Special Characters in Passwords:

        URL-encode special characters in passwords (e.g., # → %23, _ → %5F).

## 7. Appendix: SQL Queries

The dashboard uses the following SQL queries to monitor PostgreSQL performance:

[1] Top 10 Queries by Execution Time

```
SELECT query, calls, total_exec_time
FROM pg_stat_statements
WHERE query != '<insufficient privilege>'
LIMIT 10;
```

[2] Index Usage Statistics
```
SELECT schemaname, relname, indexrelname, idx_scan
FROM pg_stat_user_indexes;
```

[3] Current Locks
```
SELECT l.locktype, l.relation::regclass, l.mode, l.granted, l.pid, a.query
FROM pg_locks l
JOIN pg_stat_activity a ON l.pid = a.pid;
```

[4] Cache Hit Ratio
```
SELECT datname, (blks_hit::float / (blks_hit + blks_read + 1)) * 100 AS cache_hit_ratio
FROM pg_stat_database;
```

[5] Replication Lag
```
SELECT client_addr, state, write_lag
FROM pg_stat_replication;
```

[6] Connection Counts by State
```
SELECT state, COUNT(*)
FROM pg_stat_activity
GROUP BY state;
```

[7] Dead Tuples and Autovacuum
```
SELECT schemaname, relname, n_dead_tup, last_autovacuum
FROM pg_stat_user_tables;
```

[8] WAL Activity
```
SELECT wal_bytes, stats_reset
FROM pg_stat_wal;
```

[9] Background Writer Stats
```
SELECT checkpoints_timed, buffers_checkpoint
FROM pg_stat_bgwriter;
```

[10] Table and Index Sizes
```
SELECT relname, pg_size_pretty(pg_total_relation_size(relid))
FROM pg_stat_user_tables;
```


```
```

