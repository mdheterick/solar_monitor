#! /usr/bin/python3 -u
import urllib.request
import json
import sqlite3
import time
import os
import subprocess
import ipaddress

services_dir = os.environ["services_dir"]
inverter_mac_address = os.environ["inverter_mac_address"]
search_network = ipaddress.IPv4Network(os.environ["search_network"])


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

def check_address(address):
    ping_result = subprocess.run(["ping", "-c 1", address], capture_output=True, text=True, check=False)
    if ping_result.returncode != 0:
        return False
    result = subprocess.run(["arp", address], capture_output=True, text=True, check=True)
    return inverter_mac_address in result.stdout

if __name__ == "__main__":
    initialise_database()
    inverter_ip_address = search_network.network_address
    while True:
        try:
            try:
                if check_address(inverter_ip_address.compressed):
                    p = get_current_power(f"http://{inverter_ip_address.compressed}/solar_api/v1/GetPowerFlowRealtimeData.fcgi")
                    entry = (time.time(), p)
                    insert_solar_reading(entry)
                    print(entry)
                else:
                    for address in search_network:
                        print(f"Searching for inverter {address}")
                        if check_address(address.compressed):
                            inverter_ip_address = address
                            print(f"Found inverter at {inverter_ip_address.compressed}")
                            break
            except Exception as e:
                print("Exception: ", e)
            time.sleep(5)
        except KeyboardInterrupt:
            break
