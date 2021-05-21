#!/usr/bin/env python3
import json
import os
from dotenv import load_dotenv

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

    def write(self,data):
        dbType = os.getenv('DB_TYPE')
        if dbType == "JSON":
            return self.write_json(data)
        elif dbType == "POSTGRESQL":
            return self.write_postgre(data)
        elif dbType == "SQLITE3":
            return self.write_sqlite(data)

    def fetch_json(self):
        try:
            with open('data.json') as f:
                data = json.load(f)
                return data['data']
        except:
            print("Error while fetching JSON file")
            return "Error"

    def write_json(self, data):
        try:
            data = {'data':data}
            with open('data.json','w+') as d:
                json.dump(data, d)
            return True
        except:
            print("Error while writing to JSON")
            return False