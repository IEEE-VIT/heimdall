#!/usr/bin/env python3
import json
import os
from dotenv import load_dotenv
from os import path
import sqlite3

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

    def write(self, data, delete=False):
        dbType = os.getenv('DB_TYPE')
        if dbType == "JSON":
            return self.write_json(data,delete)
        elif dbType == "POSTGRESQL":
            return self.write_postgre(data,delete)
        elif dbType == "SQLITE3":
            return self.write_sqlite(data,delete)

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
        except:
            print("Error while fetching from SQLite3 DB")
            return {}

    def write_sqlite(self, data, delete):
        try:
            if(not(path.exists("invites.db"))):
                self.createSQLiteDB()
            con = sqlite3.connect('invites.db')
            cur = con.cursor()
            if(delete):
                cur.execute(f'DELETE FROM invites WHERE invite_code="{data["invite_code"]}"')
            else:
                cur.execute(f'INSERT INTO invites(invite_code, uses, role_linked, role_id) VALUES("{data["invite_code"]}", {data["uses"]}, "{data["role_linked"]}", "{data["role_id"]}")')
            con.commit()
            con.close()
            return True
        except:
            print("Error while writing to SQLite3 DB")
            return False

    def fetch_json(self):
        try:
            with open('data.json') as f:
                data = json.load(f)
                return data['data']
        except:
            print("Error while fetching JSON file")
            return "Error"

    def write_json(self, data, delete):
        try:
            old_data = self.fetch_json()
            if(delete):
                for i in range(len(old_data)):
                    if old_data[i] == data:
                        print(old_data[i])
                        old_data.pop(i)
                    elif i==len(old_data)-1:# Not Found
                        print("Invite Code Not Found.")
                        raise Exception()
            else:
                old_data.append(data)
            data = {'data':old_data}
            with open('data.json','w+') as d:
                json.dump(data, d)
            return True
        except:
            print("Error while writing to JSON")
            return False