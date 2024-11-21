import unittest
from datetime import datetime
from data_processing import load_gps_data


class TestGPSDataIntegrity(unittest.TestCase):

    def setUp(self):
        """Load all GPS data from the JSON file."""
        self.gps_data = load_gps_data("gps_data.json")

    def test_unique_frames(self):
        """Test that all frames in GPS data are unique."""
        seen_frames = set()
        for frame in self.gps_data:
            frame_tuple = (frame['latitude'], frame['longitude'], frame['time_utc'])
            self.assertNotIn(frame_tuple, seen_frames, f"Duplicate frame found: {frame}")
            seen_frames.add(frame_tuple)

    def test_coordinate_changes(self):
        """Test that GPS coordinates change over time."""
        for i in range(1, len(self.gps_data)):
            prev_frame = self.gps_data[i - 1]
            current_frame = self.gps_data[i]

            # Coordinates must change between consecutive frames
            self.assertNotEqual(
                (prev_frame['latitude'], prev_frame['longitude']),
                (current_frame['latitude'], current_frame['longitude']),
                f"Stationary GPS detected at frame {i}: {current_frame}"
            )

    def test_realistic_speed(self):
        """Test that speeds reported by GPS are realistic."""
        for frame in self.gps_data:
            speed = frame.get('speed_kmh', 0)
            self.assertTrue(
                0 <= speed <= 300,
                f"Unrealistic speed detected: {speed} km/h in frame {frame}"
            )

    def test_realistic_altitude(self):
        """Test that altitude values are within a realistic range."""
        for frame in self.gps_data:
            altitude = frame.get('altitude', 0)
            self.assertTrue(
                0 <= altitude <= 1000,
                f"Unrealistic altitude detected: {altitude} m in frame {frame}"
            )

    def test_time_continuity(self):
        """Test that timestamps are in chronological order."""
        for i in range(1, len(self.gps_data)):
            prev_time_str = self.gps_data[i - 1]['time_utc']
            current_time_str = self.gps_data[i]['time_utc']

            prev_time = datetime.strptime(prev_time_str, "%Y-%m-%dT%H:%M:%SZ")
            current_time = datetime.strptime(current_time_str, "%Y-%m-%dT%H:%M:%SZ")

            # Time must be in ascending order
            self.assertLess(
                prev_time,
                current_time,
                f"Timestamps out of order: {prev_time_str} -> {current_time_str}"
            )


if __name__ == "__main__":
    unittest.main()
