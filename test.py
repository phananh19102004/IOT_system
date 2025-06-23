import requests

urls = [
    "https://api.openaq.org/v3/locations/2161320/latest",
    "https://api.openaq.org/v3/locations/2161296/latest",
    "https://api.openaq.org/v3/locations/2161292/latest",
    "https://api.openaq.org/v3/locations/2161306/latest",
    "https://api.openaq.org/v3/locations/2161290/latest"
]

headers = {
    "X-API-Key": "Paste your API key here"
}

def process_url(url):
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        results = data.get("results", [])

        for result in results:
            location_name = result.get("name")
            location_id = result.get("id")
            coordinates = result.get("coordinates", {})
            latitude = coordinates.get("latitude")
            longitude = coordinates.get("longitude")

            print(f"✅ Data from {url}")
            print(f"Location: {location_name} (ID: {location_id})")
            print(f"Coordinates: ({latitude}, {longitude})")

            measurements = result.get("parameters", [])
            for m in measurements:
                parameter = m.get("parameter")
                value = m.get("lastValue")
                unit = m.get("unit")
                last_updated = m.get("lastUpdated")

                print(f" - {parameter}: {value} {unit} (Updated: {last_updated})")
            print("-" * 50)
    else:
        print(f"❌ Failed to get data from {url} - Status code: {response.status_code}")

# Gọi từng URL
for url in urls:
    process_url(url)
