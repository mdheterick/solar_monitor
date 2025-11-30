#! /usr/bin/python3 -u
from datetime import datetime, date, time
from aiohttp import web
import json
import os

services_dir = os.environ["services_dir"]

import monitor
# web server to read entries from db

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "*"
}

def filter_results(data, granularity):
    result = []
    previous_reading = None
    for [timestamp, reading] in data:
        rounded = granularity * round(reading / granularity)
        if rounded != previous_reading:
            previous_reading = rounded
            result.append([timestamp, reading])
    return result

def index(request):
    return web.FileResponse(services_dir + 'client/dist/index.html')

def get_between(start: float, end: float):
    with monitor.SolarMonitorDatabase() as db:
        a = db.cursor.execute(f"SELECT * FROM {db.table} WHERE timestamp BETWEEN ? AND ?", (start, end)).fetchall()
        return web.json_response(filter_results(a, 5), headers=CORS_HEADERS)

def get_today(request):
    today = date.today()
    start_of_day = datetime.combine(today, time.min).timestamp()
    end_of_day = datetime.combine(today, time.max).timestamp()

    return get_between(start_of_day, end_of_day)

def get_day_solar(request):
    year, month, day = request.match_info["date"].split("-")
    day_to_query = date(int(year), int(month), int(day))
    start_of_day = datetime.combine(day_to_query, time.min).timestamp()
    end_of_day = datetime.combine(day_to_query, time.max).timestamp()

    return get_between(start_of_day, end_of_day)


app = web.Application()
app.add_routes([
    web.get("/", index),
    web.get("/today", get_today),
    web.get("/solar/day/{date}", get_day_solar),
    web.static("/", services_dir + "client/dist/"),
])

web.run_app(app)
