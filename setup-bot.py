#!/usr/bin/env python3
import os
from getpass import getpass
import configparser

config = configparser.ConfigParser()
config['HEIMDALL'] = {}
dbs = ['JSON','SQLITE3','POSTGRESQL','MYSQL','MONGODB']
print('Welcome to Heimdall!')

def setup():
    config['HEIMDALL']['BOT_PREFIX'] = input('Enter the Bot Prefix(end with $): ')
    if('$' not in config['HEIMDALL']['BOT_PREFIX']):
        print('Error: $ not found in Prefix. Re-run the program.')
        exit(0)
    config['HEIMDALL']['BOT_TOKEN'] = input('Enter the Bot Token: ')

    dbtype = int(input('\nDB Type: \n1)JSON(*)\n2)SQLite3\n3)PostgreSQL\n4)MySQL\n5)MongoDB\nEnter option: '))
    dbtype = dbtype if 6>dbtype>0 else 1
    dbtype = dbs[dbtype-1]
    config['DATABASE'] = {}
    config['DATABASE']['DB_TYPE'] = dbtype

    if(dbtype == 'POSTGRESQL'):
        print('\nPostgreSQL Connection Details\n')
        config['DATABASE']['PG_HOST'] = input('Host Address: ')
        config['DATABASE']['PG_PORT'] = input('Port: ')
        config['DATABASE']['PG_USER'] = input('Username: ')
        config['DATABASE']['PG_PASS'] = input('Password: ')
        config['DATABASE']['PG_DBNAME'] = input('Database Name: ')
    elif(dbtype == 'MYSQL'):
        print('\nMySQL Connection Details\n')
        config['DATABASE']['MY_HOST'] = input('Host Address: ')
        config['DATABASE']['MY_PORT'] = input('Port: ')
        config['DATABASE']['MY_USER'] = input('Username: ')
        config['DATABASE']['MY_PASS'] = input('Password: ')
        config['DATABASE']['MY_DBNAME'] = input('Database Name: ')
    elif(dbtype == 'MONGODB'):
        config['DATABASE']['MONGO_URL'] = input('MongoDB Connection URL: ')
    config['HEIMDALL']['SETUP'] = '1'

setup()

with open('heimdall.conf','w') as configFile:
    config.write(configFile)
    print('Configs written to heimdall.conf')