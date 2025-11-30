#! /usr/bin/python3 -u
import urllib.request
import json
import sqlite3
import time
import os

services_dir = os.environ["services_dir"]


def initialise_database():
    connection = sqlite3.connect(services_dir + "solar.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS solar(timestamp INT, power INT)")
    connection.commit()
    connection.close()


class SolarMonitorDatabase:
    def __init__(self, database="solar.db", table="solar"):
        self.connection = None
        self.database = database
        self.table = table

    def __enter__(self):
        self.connection = sqlite3.connect(services_dir + self.database)
        self.cursor = self.connection.cursor()
        return self
    
    def __exit__(self, type, value, traceback):
        try:
            self.connection.commit()
        finally:
            if self.connection:
                self.connection.close()


def insert_solar_reading(entry):
    with SolarMonitorDatabase() as db:
        db.cursor.execute(f"INSERT INTO {db.table} VALUES (?, ?)", entry)


def get_current_power(url):
    with urllib.request.urlopen(url, timeout=5) as response:
        result = json.load(response)
        power = 0
        for inverter in result["Body"]["Data"]["Inverters"].values():
            power += inverter["P"]
        return power


if __name__ == "__main__":
    initialise_database()
    while True:
        try:
            try:
                p = get_current_power("http://192.168.4.28/solar_api/v1/GetPowerFlowRealtimeData.fcgi")
                entry = (time.time(), p)
                insert_solar_reading(entry)
                print(entry)
            except Exception as e:
                print("Exception: ", e)
            time.sleep(5)
        except KeyboardInterrupt:
            break
