# Airflow


## Pre Installation

1. create user and group

> user: airflow  
> uid: 50000  
> group: airflow  
> gid: 50000
    
    ```bash
    # centos 
    groupadd -g 50000 airflow
    useradd -u 50000 -g 50000 airflow
    ``````