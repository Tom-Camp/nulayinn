from adafruit_bme680 import Adafruit_BME680_I2C

class Mox:

    def __init__(self, i2c_bus: board.STEMMA_I2C):
        try:
            self.sensor = Adafruit_BME680_I2C(i2c_bus, debug=False)
            self.sensor.sea_level_pressure = 1013.25
            self.temperature_offset = -5
        except OSError as e:
            raise f"Sensor not found on I2C bus: {e}"
        except ValueError as e:
            raise f"Invalid sensor parameters: {e}"

    def warm_up(self, duration: int = 150):
        self.sensor.set_gas_heater(heater_temp=320, heater_time=duration)

    def get_temperature(self) -> float:
        return self.sensor.temperature + self.temperature_offset

    def get_humidity(self) -> float:
        return self.sensor.humidity

    def get_gas(self) -> int:
        return self.sensor.gas

    def get_pressure(self) -> float:
        return self.sensor.pressure

    def get_all(self) -> tuple:
        return self.get_temperature(), self.get_humidity(), self.get_gas(), self.get_pressure()
