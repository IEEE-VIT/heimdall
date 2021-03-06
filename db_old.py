#!/usr/bin/env python3
import json
import os
from dotenv import load_dotenv
from os import path
import sqlite3
import psycopg2
import mysql.connector
from pymongo import MongoClient
load_dotenv()

class Database:
    def fetch(self):
        dbType = os.getenv('DB_TYPE')
        if dbType == "JSON":
            return self.fetch_json()
        elif dbType == "POSTGRESQL":
            return self.fetch_postgre()
        elif dbType == "SQLITE3":
            return self.fetch_sqlite()
        elif dbType == "MYSQL":
            return self.fetch_mysql()
        elif dbType == "MONGODB":
            return self.fetch_mongo()
        else:
            raise Exception('Corrupted Config File')

    def write(self, data, delete=False, update=False):
        dbType = os.getenv('DB_TYPE')
        if dbType == "JSON":
            return self.write_json(data, delete,update)
        elif dbType == "POSTGRESQL":
            return self.write_postgre(data, delete,update)
        elif dbType == "SQLITE3":
            return self.write_sqlite(data, delete,update)
        elif dbType == "MYSQL":
            return self.write_mysql(data, delete, update)
        elif dbType == "MONGODB":
            return self.write_mongo(data, delete, update)
        else:
            raise Exception('Corrupted Config File')


    #-------------------
    #MARK: POSTGRESQL SECTION
    def connectToPostgre(self):
        try:
            con = psycopg2.connect(
                database = os.getenv('PG_DBNAME'),user = os.getenv('PG_USER'), password = os.getenv('PG_PASS'),host = os.getenv('PG_HOST'), port = os.getenv('PG_PORT')
            )
            return con
        except Exception as err:
            print("Error Connecting to PostgreSQL Server: ",err)

    def createPostgreDB(self):
        try:
            con = self.connectToPostgre()
            con.autocommit = True
            cur = con.cursor()
            cur.execute('CREATE TABLE IF NOT EXISTS invites(invite_code text, uses int, role_linked text, role_id text)')
            cur.close()
            con.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print('Error occured while creating PostgreSQL Table: ', error)

    def fetch_postgre(self):
        try:
            con = self.connectToPostgre()
            con.autocommit = True
            cur = con.cursor()
            cur.execute('SELECT * FROM invites')
            row = cur.fetchone()
            data = []
            while row is not None:
                data.append({"invite_code": row[0], "uses": row[1],"role_linked": row[2], "role_id": row[3]})
                row = cur.fetchone()
            con.close()
            return data
        except Exception as error:
            print(error)
            return {}
    
    def write_postgre(self,data,delete,update):
        try:
            con = self.connectToPostgre()
            con.autocommit = True
            cur = con.cursor()
            if(delete):
                cur.execute(f"DELETE FROM invites WHERE invite_code='{data['invite_code']}'")
            elif(update):
                cur.execute(f"UPDATE invites SET uses='{data['uses']}' WHERE invite_code='{data['invite_code']}'")
            else:
                cur.execute(f"INSERT INTO invites(invite_code, uses, role_linked, role_id) VALUES('{data['invite_code']}', {data['uses']}, '{data['role_linked']}', '{data['role_id']}')")
            cur.close()
            con.close()
            return True
        except psycopg2.errors.UndefinedTable as error:
            self.createPostgreDB()
            self.write_postgre(data,delete,update)
        except Exception as error:
            print(error)
            return False

    #-------------------
    #MARK: MYSQL SECTION
    def connectToMySQL(self):
        try:
            con = mysql.connector.connect(
                host = os.getenv('MY_HOST'),
                port = os.getenv('MY_PORT'),
                user = os.getenv('MY_USER'),
                password = os.getenv('MY_PASS'),
                database = os.getenv('MY_DBNAME'),
            )
            return con
        except Exception as e:
            print('Error connecting to MySQL DB',e)

    def createMySQLDB(self):
        try:
            con = self.connectToMySQL()
            con.autocommit = True
            cur = con.cursor()
            cur.execute('CREATE TABLE IF NOT EXISTS invites(invite_code varchar(100), uses int(10), role_linked varchar(100), role_id varchar(200))')
            con.close()
        except Exception as e:
            print('Error occured creating MySQL Table',e)

    def fetch_mysql(self):
        try:
            con = self.connectToMySQL()
            cur = con.cursor()
            cur.execute('SELECT * FROM invites')
            rows = cur.fetchall()
            data = []
            for row in rows:
                data.append({"invite_code": row[0], "uses": row[1],"role_linked": row[2], "role_id": row[3]})
            cur.close()
            con.close()
            return data
        except Exception as error:
            print(error)
            return {}

    def write_mysql(self,data,delete,update):
        try:
            con = self.connectToMySQL()
            con.autocommit = True
            cur = con.cursor()
            if(delete):
                cur.execute(f"DELETE FROM invites WHERE invite_code='{data['invite_code']}'")
            elif(update):
                cur.execute(f"UPDATE invites SET uses='{data['uses']}' WHERE invite_code='{data['invite_code']}'")
            else:
                cur.execute(f"INSERT INTO invites(invite_code, uses, role_linked, role_id) VALUES('{data['invite_code']}', {data['uses']}, '{data['role_linked']}', '{data['role_id']}')")
            con.close()
            return True
        except mysql.connector.Error as err:
            if err.errno == 1146:
                self.createMySQLDB()
                self.write_mysql(data,delete,update)
        except Exception as error:
            print(error)
            return False

    #---------------------
    #MARK: MONGODB SECTION
    def connectToMongo(self):
        con_string = os.getenv('MONGO_URL')
        client = MongoClient(con_string)
        database =  client['heimdall']
        return database['invites']

    def fetch_mongo(self):
        try:
            collection = self.connectToMongo()
            data = []
            for doc in collection.find():
                data.append(doc)
            return data
        except Exception as error:
            print(error)
            return False

    def write_mongo(self,data,delete,update):
        try:
            collection = self.connectToMongo()
            if(delete):
                collection.delete_one({'invite_code':data['invite_code']})
            elif(update):
                collection.update_one({'invite_code':data['invite_code']}, {'$set': {'uses':data['uses']}})
            else:
                collection.insert_one(data)
            return True
        except Exception as error:
            print(error)
            return False

    #---------------------
    #MARK: SQLITE3 SECTION
    def createSQLiteDB(self):
        con = sqlite3.connect('invites.db')
        cur = con.cursor()
        cur.execute('CREATE TABLE invites(invite_code text, uses int, role_linked text, role_id text)')
        con.commit()
        con.close()
        print("Created Invites DB!")

    def fetch_sqlite(self):
        try:
            if(not(path.exists("invites.db"))):
                return {}
            con = sqlite3.connect('invites.db')
            cur = con.cursor()
            result = cur.execute('SELECT * FROM invites').fetchall()
            data = []
            for row in result:
                data.append({"invite_code": row[0], "uses": row[1],"role_linked": row[2], "role_id": row[3]})
            con.commit()
            con.close()
            return data
        except Exception as error:
            print("Error while fetching from SQLite3 DB: ",error)
            return {}

    def write_sqlite(self, data, delete, update):
        try:
            if(not(path.exists("invites.db"))):
                self.createSQLiteDB()
            con = sqlite3.connect('invites.db')
            cur = con.cursor()
            if(delete):
                cur.execute(f'DELETE FROM invites WHERE invite_code="{data["invite_code"]}"')
            elif(update):
                cur.execute(f'UPDATE invites SET uses="{data["uses"]}" WHERE invite_code="{data["invite_code"]}"')
            else:
                cur.execute(f'INSERT INTO invites(invite_code, uses, role_linked, role_id) VALUES("{data["invite_code"]}", {data["uses"]}, "{data["role_linked"]}", "{data["role_id"]}")')
            con.commit()
            con.close()
            return True
        except Exception as error:
            print("Error while writing to SQLite3 DB: ",error)
            return False

    #-------------------
    #MARK: JSON SECTION
    def fetch_json(self):
        try:
            with open('data.json') as f:
                data = json.load(f)
                return data['data']
        except Exception as error:
            print("Error while fetching JSON file: ",error)
            return "Error"

    def write_json(self, data, delete, update):
        try:
            old_data = self.fetch_json()
            if(delete):
                for i in range(len(old_data)):
                    if old_data[i] == data:
                        old_data.pop(i)
                    elif i==len(old_data)-1:# Not Found
                        print("Invite Code Not Found.")
                        raise Exception()
            elif(update):
                for i in range(len(old_data)):
                    if old_data[i]['invite_code'] == data['invite_code']:
                        old_data[i] = data
                        break
            else:
                old_data.append(data)
            data = {'data':old_data}
            with open('data.json','w+') as d:
                json.dump(data, d)
            return True
        except Exception as error:
            print("Error while writing to JSON: ",error)
            return False