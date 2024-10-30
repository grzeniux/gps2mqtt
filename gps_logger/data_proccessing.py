import json
import folium
from folium.plugins import TimestampedGeoJson

# Odczytaj dane GPS z pliku JSON
try:
    with open("gps_data.json", "r") as f:
        gps_data = json.load(f)
except FileNotFoundError:
    print("Plik 'gps_data.json' nie został znaleziony.")
    exit(1)

# Tworzenie struktury dla TimestampedGeoJson
features_geojson = []
for entry in gps_data:
    # Konwersja pola 'time_utc' na timestamp do animacji
    timestamp = entry['time_utc']

    features_geojson.append({
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': [entry['longitude'], entry['latitude']],
        },
        'properties': {
            'time': timestamp,
            'speed_kmh': entry.get('speed_kmh', '---'),
            'altitude': entry.get('altitude', '---'),
            'sats': entry.get('sats', '---'),
            'style': {
                'color': 'blue' if entry.get('speed_kmh', 0) < 2 else 
                         'green' if entry.get('speed_kmh', 0) < 4 else 
                         'orange' if entry.get('speed_kmh', 0) < 8 else 
                         'red'
            },
            'icon': 'circle',
            'iconstyle': {
                'fillColor': 'blue' if entry.get('speed_kmh', 0) < 2 else 
                             'green' if entry.get('speed_kmh', 0) < 4 else 
                             'orange' if entry.get('speed_kmh', 0) < 8 else 
                             'red',
                'fillOpacity': 0.8,
                'stroke': 'true',
                'radius': 5
            }
        }
    })

# Utwórz mapę z punktami
start_location = [features_geojson[0]['geometry']['coordinates'][1], features_geojson[0]['geometry']['coordinates'][0]]
race_map = folium.Map(location=start_location, zoom_start=15)

# Dodaj animowany TimestampedGeoJson do mapy
timestamped_geojson = TimestampedGeoJson({
    'type': 'FeatureCollection',
    'features': features_geojson,
}, period='PT10S', add_last_point=True)
timestamped_geojson.add_to(race_map)

# Dodaj ramkę telemetryczną do mapy z aktualizacją danych
race_map.get_root().html.add_child(folium.Element(f'''
    <div id="telemetry-data" style="position: fixed; top: 20px; right: 20px; 
        background-color: rgba(255, 255, 255, 0.8); padding: 10px; border: 2px solid black; z-index: 1000; width: 250px;">
        <h4>Telemetry Data</h4>
        <p><strong>Time (UTC):</strong> <span id="telemetry-time">---</span></p>
        <p><strong>Speed:</strong> <span id="telemetry-speed">---</span> km/h</p>
        <p><strong>Satellite Count:</strong> <span id="telemetry-satellites">---</span></p>
        <p><strong>Altitude:</strong> <span id="telemetry-altitude">---</span> m</p>
    </div>
    <script>
        document.addEventListener('DOMContentLoaded', function () {{
            let markersData = {json.dumps(features_geojson)};  // Dane JSON przekazane do skryptu

            // Funkcja aktualizująca dane telemetryczne w ramce
            function updateTelemetryData(properties) {{
                document.getElementById("telemetry-time").innerText = properties.time || '---';
                document.getElementById("telemetry-speed").innerText = properties.speed_kmh || '---';
                document.getElementById("telemetry-satellites").innerText = properties.sats || '---';
                document.getElementById("telemetry-altitude").innerText = properties.altitude || '---';
                console.log("Telemetry data updated:", properties);
            }}

            // Funkcja animująca markery na podstawie timestampów
            function startAnimation() {{
                let index = 0;

                function animate() {{
                    if (index < markersData.length) {{
                        const marker = markersData[index];
                        setTimeout(() => {{
                            updateTelemetryData(marker.properties);
                            index++;
                            animate();
                        }}, 500);  // Zmieniaj czas opóźnienia w zależności od potrzeb
                    }}
                }}
                animate();
            }}

            // Start animacji po załadowaniu danych
            startAnimation();
        }});
    </script>
'''))

# Zapisz mapę do pliku HTML
race_map.save("animated_map_with_telemetry.html")
print("Mapa z animacją i ramką telemetryczną została zapisana jako 'animated_map_with_telemetry.html'")
