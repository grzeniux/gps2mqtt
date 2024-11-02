import json
import folium
from folium.plugins import TimestampedGeoJson
from datetime import datetime
import pytz

try:
    with open("gps_data.json", "r") as f:
        gps_data = json.load(f)
except FileNotFoundError:
    print("File 'gps_data.json' not found.")
    exit(1)

utc_tz = pytz.utc
poland_tz = pytz.timezone('Europe/Warsaw')

# Prepare data for TimestampedGeoJson
features_geojson = []
for entry in gps_data:
    timestamp_utc = datetime.strptime(entry['time_utc'], "%Y-%m-%dT%H:%M:%SZ")
    timestamp_local = timestamp_utc.replace(tzinfo=utc_tz).astimezone(poland_tz)
    timestamp_local_str = timestamp_local.strftime("%Y-%m-%d %H:%M:%S")  # Format the time as needed
    
    speed = entry.get('speed_kmh', 0)
    if speed <= 2:
        color = 'blue'
    else:
        color = next(color for threshold, color in [(4, 'green'), (8, 'orange'), (float('inf'), 'red')] if speed < threshold)
    
    # Popup content with converted time
    popup_content = f"Time (Local): {timestamp_local_str}<br>Speed: {speed} km/h<br>Satellite Count: {entry.get('sats', '---')}<br>Altitude: {entry.get('altitude', '---')} m"

    # Add properties for each point
    features_geojson.append({
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': [entry['longitude'], entry['latitude']],
        },
        'properties': {
            'time': timestamp_local_str,  # Use local time for the animation
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

# Create map with starting location
start_location = [features_geojson[0]['geometry']['coordinates'][1], features_geojson[0]['geometry']['coordinates'][0]]
race_map = folium.Map(location=start_location, zoom_start=15)

# Add TimestampedGeoJson to the map
timestamped_geojson = TimestampedGeoJson({
    'type': 'FeatureCollection',
    'features': features_geojson,
}, period='PT10S', add_last_point=True)
timestamped_geojson.add_to(race_map)

race_map.save("animated_map_with_polish_time.html")
print("Map with animation and clickable popups saved as 'animated_map_with_polish_time.html'")
