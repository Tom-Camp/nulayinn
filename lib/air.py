from adafruit_ahtx0 import AHTx0

class Air:

    def __init__(self, i2c_bus: board.I2C):
        try:
            self.sensor = AHTx0(i2c_bus)
            print("AHT sensor initialized successfully")
        except OSError as e:
            raise f"Sensor not found on I2C bus: {e}"
        except ValueError as e:
            raise f"Invalid sensor parameters: {e}"
    def read_temperature(self) -> float | None:
        """
        Read temperature in Celsius
        :return: float: Temperature in Celsius, or None if read fails
        """
        try:
            temp = self.sensor.temperature
            return round(temp, 1)
        except Exception as e:
            print(f"Error reading temperature: {e}")
            return None

    def read_humidity(self) -> float | None:
        """
        Read relative humidity
        :return: float: Relative humidity percentage, or None if read fails
        """
        try:
            humidity = self.sensor.relative_humidity
            return round(humidity, 1)
        except Exception as e:
            print(f"Error reading humidity: {e}")
            return None

    def read_all(self) -> tuple:
        """
        Read both temperature and humidity
        :return: tuple: (temperature, humidity) or (None, None) if read fails
        """
        return self.read_temperature(), self.read_humidity()