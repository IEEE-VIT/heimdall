#!/usr/bin/env python3
import sys
import dotenv
import os
from getpass import getpass

dotenv.load_dotenv()
dbs = ['JSON','SQLITE3','POSTGRESQL','MYSQL','MONGODB']
print('Welcome to PRooster!')

def setup():
    os.putenv('BOT_PREFIX',input('Enter the Bot Prefix: '))
    os.putenv( 'BOT_TOKEN', input('Enter the Bot Token: '))

    dbtype = int(input('\nDB Type: \n1)JSON(*)\n2)SQLite3\n3)PostgreSQL\n4)MySQL\n5)MongoDB\nEnter option: '))
    dbtype = dbtype if 6>dbtype>0 else 1
    dbtype = dbs[dbtype-1]
    os.putenv( 'DB_TYPE', dbtype)

    if(dbtype == 'POSTGRESQL'):
        print('\nPostgreSQL Connection Details\n')
        os.putenv( 'PG_HOST', input('Host Address: '))
        os.putenv( 'PG_PORT', input('Port: '))
        os.putenv( 'PG_USER', input('Username: '))
        os.putenv( 'PG_PASS', input('Password: '))
        os.putenv( 'PG_DBNAME', input('Database Name: '))
    elif(dbtype == 'MYSQL'):
        print('\nMySQL Connection Details\n')
        os.putenv( 'MY_HOST', input('Host Address: '))
        os.putenv( 'MY_PORT', input('Port: '))
        os.putenv( 'MY_USER', input('Username: '))
        os.putenv( 'MY_PASS', input('Password: '))
        os.putenv( 'MY_DBNAME', input('Database Name: '))
    elif(dbtype == 'MONGODB'):
        os.putenv( 'MONGO_URL', input('MongoDB Connection URL: '))
    os.putenv( 'SETUP', '1')
def help():
    print('Usage:\n-h --help\t: Help\n-c --configure\t: Configure the bot with the bot token and database type and details.')

try:
    if(sys.argv[1] == '--help' or sys.argv[1]=='-h'):
        help()
        exit(0)
    elif(int(os.environ['SETUP']) == 0 or sys.argv[1] == '--configure' or sys.argv[1] == '-c'):
        setup()
except IndexError:
    pass

#dotenv.load_dotenv(env)
print('\nRunning the bot...\n')
os.system('python3 client.py &')
os.system('python3 bot.py')