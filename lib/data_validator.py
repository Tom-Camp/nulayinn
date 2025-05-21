import json
import microcontroller
import time

class SensorDataValidator:

    def __init__(self, reading: dict):
        self.reading = reading

    def has_data(self) -> bool:
        return False if self.reading is None else True


    def validate_sensor_reading(self) -> bool:
        """
        Validate if sensor reading is within acceptable range
        Returns True if valid, False if invalid
        """
        try:
            valid_ranges: dict = {
                "air_temp": (-40, 85),  # °C
                "air_humidity": (0, 100),  # %
                "pressure": (300, 1100),  # hPa
                "gas": (0, 500000), # ohm
                "temp": (-40, 85), # °C
                "humidity": (0, 100), # %
            }
            for key, value in self.reading.items():
                if key in valid_ranges:
                    min_val, max_val = valid_ranges.get(key)
                    if not isinstance(value, (int, float)) or value < min_val or value > max_val:
                        print(f"Invalid {key} reading: {value}")
                        return False

            return True

        except Exception as e:
            print(f"Validation error: {e}")
            return False

    def prepare_transmission_data(self) -> bytes | None:
        """
        Prepare and validate data for transmission
        """
        try:
            json_data = json.dumps(self.reading)
            test_decode = json.loads(json_data)
            if not all(key in test_decode for key in self.reading.keys()):
                return None

            return json_data.encode("utf-8")

        except TypeError as e:
            print(f"Data preparation error: {e}")
            return None

    @staticmethod
    def hard_reset():
        """
        Perform a clean reload of the system
        """
        print("Performing system reset...")
        time.sleep(1)
        microcontroller.reset()