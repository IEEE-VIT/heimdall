#!/usr/bin/env python3
import json
import os
from dotenv import load_dotenv
from os import path
import sqlite3
import psycopg2
import mysql.connector
from pymongo import MongoClient
from abc import ABC, abstractmethod
load_dotenv()

class Database(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def fetchall(self):
        pass

    @abstractmethod
    def fetchone(self, row, where = None):
        pass

    @abstractmethod
    def insert(self, row):
        pass

    @abstractmethod
    def delete(self, row):
        pass

    @abstractmethod
    def update(self, row, where = None):
        pass

    def choose():
        dbType = os.getenv('DB_TYPE')
        if dbType == "JSON":
            dbObj = JSON()
        elif dbType == "POSTGRESQL":
            dbObj = PostgreSQL()
        elif dbType == "SQLITE3":
            dbObj = SQLite3()
        elif dbType == "MYSQL":
            dbObj = MySQL()
        elif dbType == "MONGODB":
            dbObj = MongoDB()
        else:
            print(dbType)
            raise Exception('Corrupted Config File')
        return dbObj

class MySQL(Database):

    def connect(self):
        try:
            con = mysql.connector.connect(
                host = os.getenv('MY_HOST'),
                port = os.getenv('MY_PORT'),
                user = os.getenv('MY_USER'),
                password = os.getenv('MY_PASS'),
                database = os.getenv('MY_DBNAME'),
            )
            con.autocommit = True
            cur = con.cursor()
            cur.execute('CREATE TABLE IF NOT EXISTS invites(invite_code varchar(100) primary key, uses int(10), role_linked varchar(100), role_id varchar(200))')
            return con
        except Exception as e:
            print('Error connecting to MySQL DB',e)
    
    def fetchall(self):
        try:
            con = self.connect()
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
    
    def fetchone(self, column, where=None):
        try:
            con = self.connect()
            cur = con.cursor()
            column = ','.join(column)
            if(where == None):
                cur.execute(f'SELECT {column} FROM invites')
            else:
                where_clause = f'WHERE {list(where.keys())[0]} = "{list(where.values())[0]}"'
                cur.execute(f'SELECT {column} FROM invites {where_clause}')
            rows = cur.fetchall()
            data = {'data':[]}
            for row in rows:
                if(len(row)>1):
                    data[row[0]]=row[1]
                else:
                    data['data'].append(row[0])
            return data
        except Exception as e:
            print(e)
            return {}

    def insert(self, data):
        try:
            con = self.connect()
            con.autocommit = True
            cur = con.cursor()
            cur.execute(f"INSERT INTO invites(invite_code, uses, role_linked, role_id) VALUES('{data['invite_code']}', {data['uses']}, '{data['role_linked']}', '{data['role_id']}')")
            con.close()
            return True
        except mysql.connector.Error as err:
            if err.errno == 1146:
                self.createMySQLDB()
                self.insert(data)
        except Exception as error:
            print(error)
            return False

    def update(self, set, where):
        try:
            con = self.connect()
            con.autocommit = True
            cur = con.cursor()
            cur.execute(f"UPDATE invites SET {list(set.keys())[0]}='{list(set.values())[0]}' WHERE {list(where.keys())[0]}='{list(where.values())[0]}'")
            con.close()
            return True
        except Exception as error:
            print(error)
            return False

    def delete(self, where):
        try:
            con = self.connect()
            con.autocommit = True
            cur = con.cursor()
            where_clause = f'WHERE {list(where.keys())[0]}="{list(where.values())[0]}"'
            cur.execute(f'DELETE FROM invites {where_clause}')
            return True
        except Exception as e:
            print(e)
            return False

class PostgreSQL(Database):

    def connect(self):
        try:
            con = psycopg2.connect(
                database = os.getenv('PG_DBNAME'),user = os.getenv('PG_USER'), password = os.getenv('PG_PASS'),host = os.getenv('PG_HOST'), port = os.getenv('PG_PORT')
            )
            con.autocommit = True
            cur = con.cursor()
            cur.execute('CREATE TABLE IF NOT EXISTS invites(invite_code text primary key, uses int, role_linked text, role_id text)')
            return con
        except (Exception, psycopg2.DatabaseError) as error:
            print('Error occured while creating PostgreSQL Table: ', error)
            return False
        except Exception as err:
            print("Error Connecting to PostgreSQL Server: ",err)
    
    def fetchall(self):
        try:
            con = self.connect()
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

    def fetchone(self, column, where=None):
        try:
            con = self.connect()
            cur = con.cursor()
            column = ','.join(column)
            if(where == None):
                cur.execute(f'SELECT {column} FROM invites')
            else:
                where_clause = f"WHERE {list(where.keys())[0]} = '{list(where.values())[0]}'"
                cur.execute(f'SELECT {column} FROM invites {where_clause}')
            rows = cur.fetchall()
            data = {'data':[]}
            for row in rows:
                if(len(row)>1):
                    data[row[0]]=row[1]
                else:
                    data['data'].append(row[0])
            return data
        except Exception as e:
            print(e)
            return {}

    def insert(self, data):
        try:
            con = self.connect()
            con.autocommit = True
            cur = con.cursor()
            cur.execute(f"INSERT INTO invites(invite_code, uses, role_linked, role_id) VALUES('{data['invite_code']}', {data['uses']}, '{data['role_linked']}', '{data['role_id']}')")
            con.close()
            return True
        except mysql.connector.Error as err:
            if err.errno == 1146:
                self.createMySQLDB()
                self.insert(data)
        except Exception as error:
            print(error)
            return False

    def update(self, set, where):
        try:
            con = self.connect()
            con.autocommit = True
            cur = con.cursor()
            cur.execute(f"UPDATE invites SET {list(set.keys())[0]}='{list(set.values())[0]}' WHERE {list(where.keys())[0]}='{list(where.values())[0]}'")
            con.close()
            return True
        except Exception as error:
            print(error)
            return False

    def delete(self, where):
        try:
            con = self.connect()
            con.autocommit = True
            cur = con.cursor()
            where_clause = f"WHERE {list(where.keys())[0]}='{list(where.values())[0]}'"
            cur.execute(f"DELETE FROM invites {where_clause}")
            return True
        except Exception as e:
            print(e)
            return False

class JSON(Database):

    def connect(self):
        try:
            f = open('data.json')
            data = json.load(f)
            return data['data']
        except Exception as error:
            print('Error while fetching JSON file:', error)
            return False

    def fetchall(self):
        try:
            data = self.connect()
            return data
        except Exception as error:
            print("Error while fetching JSON file: ",error)
            return False
    
    def fetchone(self, row, where=None):
        try:
            data = self.connect()
            rows = {'data':[]}
            if where == None:
                for line in data:
                    if(type(row)==list and len(row)>1):
                        rows[line[row[0]]] = line[row[1]]
                    else:
                        rows['data'].append(line[row[0]])
                return rows
            else:
                for line in data:
                    if list(where.values())[0] == line[list(where.keys())[0]]:
                        if(type(row)==list and len(row)>1):
                            rows[line[row[0]]] = line[row[1]]
                        else:
                            rows['data'].append(line[row[0]])
        except Exception as error:
            print("Error while fetching JSON file: ",error)
            return False

    def insert(self, row):
        try:
            data = self.connect()
            data.append(row)
            data = {'data': data}
            with open('data.json','w+') as d:
                json.dump(data, d)
            return True
        except Exception as error:
            print("Error while inserting to JSON file: ",error)
            return False
    
    def update(self, set, where):
        try:
            data = self.connect()
            for line in data:
                if line[list(where.keys())[0]] == list(where.values())[0]:
                    line[list(set.keys())[0]] = list(set.values())[0]
            data = {'data': data}
            with open('data.json','w+') as d:
                json.dump(data, d)
            return True
        except Exception as error:
            print("Error while updating JSON file: ",error)
            return False

    def delete(self, where=None):
        try:
            data = self.connect()
            for i in range(len(data)):
                if data[i][list(where.keys())[0]] == list(where.values())[0]:
                    data.pop(i)
            data = {'data': data}
            with open('data.json','w+') as d:
                json.dump(data, d)
            return True
        except Exception as error:
            print("Error while deleting from JSON file: ",error)
            return False

class SQLite3(Database):

    def connect(self):
        try:
            con = sqlite3.connect('invites.db')
            cur = con.cursor()
            cur.execute('CREATE TABLE IF NOT EXISTS invites(invite_code text primary key, uses int, role_linked text, role_id text)')
            con.commit()
            return con
        except Exception as e:
            print('Error connecting to SQLite3 DB: ',e)
    
    def fetchall(self):
        try:
            con = self.connect()
            cur = con.cursor()
            result = cur.execute('SELECT * FROM invites').fetchall()
            data = []
            for row in result:
                data.append({"invite_code": row[0], "uses": row[1],"role_linked": row[2], "role_id": row[3]})
            con.commit()
            con.close()
            return data
        except Exception as error:
            print(error)
            return {}
    
    def fetchone(self, column, where=None):
        try:
            con = self.connect()
            cur = con.cursor()
            column = ','.join(column)
            if(where == None):
                cur.execute(f'SELECT {column} FROM invites')
            else:
                where_clause = f'WHERE {list(where.keys())[0]} = "{list(where.values())[0]}"'
                cur.execute(f'SELECT {column} FROM invites {where_clause}')
            rows = cur.fetchall()
            data = {'data':[]}
            for row in rows:
                if(len(row)>1):
                    data[row[0]]=row[1]
                else:
                    data['data'].append(row[0])
            return data
        except Exception as e:
            print(e)
            return {}

    def insert(self, data):
        try:
            con = self.connect()
            cur = con.cursor()
            cur.execute(f"INSERT INTO invites(invite_code, uses, role_linked, role_id) VALUES('{data['invite_code']}', {data['uses']}, '{data['role_linked']}', '{data['role_id']}')")
            con.commit()
            con.close()
            return True
        except mysql.connector.Error as err:
            if err.errno == 1146:
                self.createMySQLDB()
                self.insert(data)
        except Exception as error:
            print(error)
            return False

    def update(self, set, where):
        try:
            con = self.connect()
            cur = con.cursor()
            cur.execute(f"UPDATE invites SET {list(set.keys())[0]}='{list(set.values())[0]}' WHERE {list(where.keys())[0]}='{list(where.values())[0]}'")
            con.commit()
            con.close()
            return True
        except Exception as error:
            print(error)
            return False

    def delete(self, where):
        try:
            con = self.connect()
            cur = con.cursor()
            where_clause = f'WHERE {list(where.keys())[0]}="{list(where.values())[0]}"'
            cur.execute(f'DELETE FROM invites {where_clause}')
            con.commit()
            con.close()
            return True
        except Exception as e:
            print(e)
            return False

class MongoDB(Database):

    def connect(self):
        try:
            con_string = os.getenv('MONGO_URL')
            client = MongoClient(con_string)
            database =  client['rooster']
            return database['invites']
        except Exception as e:
            print('Error connecting to MongoDB: ',e)

    def fetchall(self):
        try:
            collection = self.connect()
            data = []
            for doc in collection.find():
                data.append(doc)
            return data
        except Exception as error:
            print(error)
            return {}
    
    def fetchone(self, column, where=None):
        try:
            collection = self.connect()
            data = {'data':[]}
            if(where == None):
                for doc in collection.find({}, {key: 1 for key in column}):
                    if(len(column)>1):
                        data[doc[column[0]]] = doc[column[1]]
                    else:
                        data['data'].append(doc[column])
            else:
                for doc in collection.find(where, {key: 1 for key in column}):
                    if(len(column)>1):
                        data[doc[column[0]]] = doc[column[1]]
                    else:
                        data['data'].append(doc[column])
            return data
        except Exception as e:
            print(e)
            return {}

    def insert(self, data):
        try:
            collection = self.connect()
            collection.insert_one(data)
            return True
        except Exception as error:
            print(error)
            return False

    def update(self, set, where):
        try:
            collection = self.connect()
            collection.update_one(where, {'$set': set})
            return True
        except Exception as error:
            print(error)
            return False

    def delete(self, where):
        try:
            collection = self.connect()
            collection.delete_one(where)
            return True
        except Exception as e:
            print(e)
            return False