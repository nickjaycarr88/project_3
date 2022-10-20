import pandas as pd
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine
from sqlalchemy import inspect
from SQLkeys import password

#set up connecting route

protocol = 'postgresql'
username = 'postgres'
host = 'localhost'
port = 5432
database_name = 'etl_db'

# connecting to postgresql to create a db

connection_string = f'{protocol}://{username}:{password}@{host}:{port}/'

con = psycopg2.connect(connection_string)

con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

cur = con.cursor()

cur.execute("drop database if exists ETL_db;")

cur.execute("create database ETL_db;")

cur.close()

# connecting to db to input data

rds_connection_string = f'{connection_string}{database_name}'

engine = create_engine(rds_connection_string)



try:
    #make sure we only create three tables without duplicate name 

    engine.execute("DROP TABLE IF EXISTS gdp")

    engine.execute("DROP TABLE IF EXISTS population")

    engine.execute("DROP TABLE IF EXISTS gender")

    #calling queries

    sql_gdp = '''
    CREATE TABLE gdp(countryName VARCHAR (255), "2000" float ,\
        "2001" float ,"2002" float ,"2003" float ,\
        "2004" float ,"2005" float ,"2006" float ,\
        "2007" float ,"2008" float ,"2009" float ,\
        "2010" float ,"2011" float ,"2012" float ,\
        "2013" float ,"2014" float ,"2015" float ,\
        "2016" float ,"2017" float ,"2018" float ,\
        "2019" float ,"2020" float );
    '''

    sql_pop = '''
    CREATE TABLE population(countryName VARCHAR (255), "2000" float ,\
        "2001" float ,"2002" float ,"2003" float ,\
        "2004" float ,"2005" float ,"2006" float ,\
        "2007" float ,"2008" float ,"2009" float ,\
        "2010" float ,"2011" float ,"2012" float ,\
        "2013" float ,"2014" float ,"2015" float ,\
        "2016" float ,"2017" float ,"2018" float ,\
        "2019" float ,"2020" float );
    '''

    sql_gender = '''
    CREATE TABLE gender(countryName VARCHAR (255),indicatorName VARCHAR (255),\
        "2000" float ,"2001" float ,"2002" float ,\
        "2003" float ,"2004" float ,"2005" float ,\
        "2006" float ,"2007" float ,"2008" float ,\
        "2009" float ,"2010" float ,"2011" float ,\
        "2012" float ,"2013" float ,"2014" float ,\
        "2015" float ,"2016" float ,"2017" float ,\
        "2018" float , "2019" float ,"2020" float );
    
    '''
    # execute queries to create three tables to hold three different datadsets 

    engine.execute(sql_gdp)

    engine.execute(sql_pop)

    engine.execute(sql_gender)

    # load datasets

    gdp_df = pd.read_csv('OutputData/GDP%.csv')

    gdp_df.to_sql('gdp', engine, if_exists= 'replace', index= False)

    print(f'gdp dataset has been loaded in PostgreSQL database' )

    
    pop_df = pd.read_csv('OutputData/population.csv')

    pop_df.to_sql('population', engine, if_exists= 'replace', index= False)

    print(f'population dataset has been loaded in PostgreSQL database' )

    
    gender_df = pd.read_csv('OutputData/gender.csv')

    gender_df.to_sql('gender', engine, if_exists= 'replace', index= False)

    print(f'gender dataset has been loaded in PostgreSQL database' )

except (Exception, Error) as error:

    print("Error while connecting to PostgreSQL", error)

finally:

  engine.dispose()

  print("PostgreSQL connection is closed")


