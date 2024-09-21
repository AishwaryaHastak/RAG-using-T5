# Project Directory Structure

This project consists of several important directories and files. Below is a brief explanation of the key components:

## Directory Structure

- **app/**
  - **src/**: Contains the main source code for the application, including modules for database interaction and various pipelines.
    - **db.py**: Script to initialize the postgres database, create tables and populate with data.
    - **espipeline.py**: Script for elastic search RAG pipeline with text search.
    - **vectorpipeline.py**: Script for elastic search RAG pipeline with vector search.
  - **Dockerfile**: Configuration file for building the Docker image for the Streamlit application.
  - **docker-compose.yml**: Defines the services, networks, and volumes used in the application setup.
  - **.env.example**: Template file for environment variables. Copy and rename it to `.env` to configure your environment.

## Accessing Grafana

1. Open your web browser and navigate to:
```
http://localhost:3000
```

2. Log in using the default credentials:
- **Username**: `admin`
- **Password**: `admin`

3. Once logged in, add a data source:
- Select **Data Sources** from the sidebar.
- Choose **PostgreSQL** as the data source type.
- Enter your PostgreSQL credentials (DB_USER, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT).

4. Create your dashboards to visualize your data!
