import requests
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
import time

# ======= CONFIG INFLUXDB =======
url_influx = "http://localhost:8086"
token = "oJVPlf3AWJAlJD1dfrb7dxsd0dT9VAAiYggt-TY_4DSdGRZ7tlI4iTyLQpULMyETBzwY9zlZhYn7G3VmcoIiCA=="
org = "IOT"
bucket = "TEST"

client = InfluxDBClient(url=url_influx, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

# ======= URL LIST =======
urls = [
    "https://api.openaq.org/v3/locations/2161320/latest",
    "https://api.openaq.org/v3/locations/2161296/latest",
    "https://api.openaq.org/v3/locations/2161292/latest",
    "https://api.openaq.org/v3/locations/2161306/latest",
    "https://api.openaq.org/v3/locations/2161290/latest"
]

headers = {
    "X-API-Key": "114a6ceb815538eca8ef9d507f73b31cafde4c08aca7928354b7bdcc08a3b6e6"
}

# ======= Processing URL per time =======
def process_url(url):
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        results = data["results"]

        for result in results:
            latitude = result["coordinates"]["latitude"]
            longitude = result["coordinates"]["longitude"]
            timestamp = result["datetime"]["utc"]
            value = result["value"]
            
            sensor_id = str(result.get("sensorsId", "unknown"))
            location_id = str(result.get("locationsId", "unknown"))


            point = (
                Point("air_quality")
                .tag("sensor_id", sensor_id)
                .tag("location_id", location_id)
                .field("value", float(value))
                .field("lat", float(latitude))
                .field("lon", float(longitude))
                .time(datetime.utcnow()) #time = UTC in influxdb
            )
            write_api.write(bucket=bucket, org=org, record=point)

        print(f"✅ Data from {url} inserted to InfluxDB.")
    else:
        print(f"❌ Failed to get data from {url} - Status code: {response.status_code}")

# ======= LOOP THE URL LIST =======
while True:
    for url in urls:
        process_url(url)
    time.sleep(300)  # Wait 300s
