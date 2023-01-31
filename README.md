# API GEN
Executing redundant queries repetitively can waste time, to counter this problem we have created APIGen. The main aim of our project is to analyse the existing query logs of a database and generate custom APIs that execute the recommended important queries that have been run often in the database. These APIs once run, will execute the recommended queries onto the database for efficient work.

## Prerequisites
Install the file "requirements.txt"

## Getting Started
1. pip install virtualenv
2. virtualenv env
3. cd env/Scripts/activate 
4. pip install -r requirements.txt
5. python manage.py runserver 8000 

## Functionalities
1) Support for SQL and NoSQL databases:
APIGen will access the provided query logs from both SQL and NoSQL databases, preprocess the logs and then plug these queries into our ML model.
2) Recommend APIs:
Our ML model will analyse the queries and check for the queries which have been used the 
most along with the tables that have been frequently accessed.
After processing it will generate custom APIs for the recommended queries given by the 
model. These APIs will fire the queries in the connected database whenever needed.
3) Query Analytics:
Along with the custom generated APIs, APIGen will provide several query analytics such as 
queries with the least processing time, queries with maximum processing time , mean query 
processing time.
This will help generate insights about the performance of the database and the queries 
which have been executed.

## Analysis Metrics
1) Queries taking maximum processing time and the time taken
2) Queries taking minimum processing time and the time taken
3) Mean time taken by the queries to process
4) Number of Queries Submitted over Time
5) Correlation between Execution Time And Client's IP Address
6) Top 5 Queried Table
7) Load on Database by Client's IP Address
