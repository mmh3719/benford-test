# Benford's Law

Basic app that takes in a file with columnar data and a column name and creates a bar chart comparing the percentage 
occurrence of leading digits and compares it to those expected by Benford's Law.

The title of the bar chart says whether or not the data fits the expected values from Benford's Law.

## Running application

This application can run in a docker container using docker-compose.

Simply do the following:
```shell script
docker-compose build
docker-compose up
```
