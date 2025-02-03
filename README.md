# Postgres Monitoring Dashboard
A Real-Time Monitoring Dashboard for PostgreSQL 

# Deployment Guide: PostgreSQL Monitoring Dashboard with FastAPI and Docker

This guide provides step-by-step instructions to deploy a PostgreSQL monitoring dashboard using FastAPI, Docker, and pg_stat_statements. The dashboard allows you to monitor the performance of multiple PostgreSQL databases and visualize key metrics.

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

## 3. Build and Deploy the FastAPI Application

Clone the repository containing the FastAPI application:

```
git clone https://github.com/shadabshaukat/postgres-monitoring.git
cd postgres-monitoring
```

Set Up Environment Variables

```
export DATABASES='{"prod_db":"postgresql://postgres:RAbbithole1234%23%5F@10.180.2.171:5432/postgres","stage_db":"postgresql://postgres:RAbbithole1234%23%5F@10.180.2.228:5432/dvdrental"}'
```

Replace the connection strings with your actual database credentials. URL-encode special characters in passwords (e.g., # → %23, _ → %5F). Ref : https://www.w3schools.com/tags/ref_urlencode.ASP 

Alternately you can use a .env file in your docker container. First create a .env file

```
echo 'DATABASES={"prod_db":"postgresql://postgres:RAbbithole1234%23%5F@10.180.2.171:5432/postgres","stage_db":"postgresql://postgres:RAbbithole1234%23%5F@10.180.2.228:5432/dvdrental"}' > .env
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

        psql "postgresql://postgres:RAbbithole1234%23%5F@10.180.2.171:5432/postgres"

Special Characters in Passwords:

        URL-encode special characters in passwords (e.g., # → %23, _ → %5F).
