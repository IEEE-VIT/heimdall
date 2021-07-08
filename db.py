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
                    if data[i] == data:
                        data.pop(i)
                        return True
                return False
            else:
                old_data.append(data)
                data = {'data':old_data}
                print(data)
                with open('data.json','w+') as d:
                    json.dump(data, d)
                return True
        except:
            print("Error while writing to JSON")
            return False