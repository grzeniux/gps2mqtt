import json
import folium
from folium.plugins import TimestampedGeoJson
from datetime import datetime
import pytz

def load_gps_data(file_path="gps_data.json"):
    """Load GPS data from a JSON file."""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File '{file_path}' not found")
        exit(1)

def convert_to_local_time(timestamp_utc_str, timezone_str='Europe/Warsaw'):
    """Convert UTC timestamp to local time."""
    utc_tz = pytz.utc
    local_tz = pytz.timezone(timezone_str)
    timestamp_utc = datetime.strptime(timestamp_utc_str, "%Y-%m-%dT%H:%M:%SZ")
    return timestamp_utc.replace(tzinfo=utc_tz).astimezone(local_tz)

def get_marker_color(speed):
    """Determine the marker color based on speed."""
    if speed <= 2:
        return 'blue'
    elif speed <= 4:
        return 'green'
    elif speed <= 8:
        return 'orange'
    else:
        return 'red'

def prepare_geojson_features(gps_data, timezone_str='Europe/Warsaw'):
    """Prepare GeoJSON features from GPS data."""
    features_geojson = []
    for entry in gps_data:
        timestamp_local = convert_to_local_time(entry['time_utc'], timezone_str)
        timestamp_local_str = timestamp_local.strftime("%Y-%m-%d %H:%M:%S")

        speed = entry.get('speed_kmh', 0)
        color = get_marker_color(speed)

        popup_content = (
            f"Time (Local): {timestamp_local_str}<br>"
            f"Speed: {speed} km/h<br>"
            f"Satellite Count: {entry.get('sats', '---')}<br>"
            f"Altitude: {entry.get('altitude', '---')} m"
        )

        features_geojson.append({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [entry['longitude'], entry['latitude']],
            },
            'properties': {
                'time': timestamp_local_str,
                'speed_kmh': speed,
                'altitude': entry.get('altitude', '---'),
                'sats': entry.get('sats', '---'),
                'popup': popup_content,
                'style': {
                    'color': color
                },
                'icon': 'circle',
                'iconstyle': {
                    'fillColor': color,
                    'fillOpacity': 0.8,
                    'stroke': 'true',
                    'radius': 5
                }
            }
        })
    return features_geojson

def create_map(features_geojson, output_file="animated_map.html"):
    """Create a map with TimestampedGeoJson and save it to a file."""
    start_location = [
        features_geojson[0]['geometry']['coordinates'][1],
        features_geojson[0]['geometry']['coordinates'][0]
    ]
    race_map = folium.Map(location=start_location, zoom_start=15)

    timestamped_geojson = TimestampedGeoJson({
        'type': 'FeatureCollection',
        'features': features_geojson,
    }, period='PT10S', add_last_point=True)
    timestamped_geojson.add_to(race_map)

    race_map.save(output_file)
    print(f"Map with animation and clickable popups saved as '{output_file}'")


if __name__ == "__main__":
    gps_data = load_gps_data()
    features_geojson = prepare_geojson_features(gps_data)
    create_map(features_geojson)
