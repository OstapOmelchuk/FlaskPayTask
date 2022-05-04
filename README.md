# Environment variables
___
create .env file and add:
    
    POSTGRES_USER=<your_username>       # str type
    POSTGRES_PASSWORD=<your_password>       # str type
    POSTGRES_DB='<db_name>'        # str type
    POSTGRES_HOST='your_postgres_host>'        # for example 'localhost'

    SQLALCHEMY_DATABASE_URI='postgresql://<your_username>:<your_password>@<your_postgres_host>/<db_name>'
    SECRET_KEY=<your_secret_key>
---

# Installation of necessary packages

To install all the packages activate your virtualenv and run the following command in your terminal:
    
    pip install -r requirements.txt


---
# Creating a database and table

To create DB - type in your terminal:

    createdb -h <your_postgres_host> -p <your_postgres_port> -U <your_username> <db_name>

    # for example: createdb -h localhost -p 5432 -U postgres VocabularyTask

To create a table in your DB just run a run.py file and the table automatically will be created if it did not exist

