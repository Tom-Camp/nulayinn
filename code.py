import alarm
import board
import busio
import os
import time

from adafruit_ahtx0 import AHTx0
from adafruit_bme680 import Adafruit_BME680_I2C

from lib.lora_sender import LoraSender
from lib.battery_monitor import BatteryMonitor


def sleep(duration: int = 3600):
    time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + duration)
    alarm.exit_and_deep_sleep_until_alarms(time_alarm)


def celsius_to_fahrenheit(celsius: float) -> float:
    return (celsius * 9 / 5) + 32


battery = BatteryMonitor()
voltage: float = 0.0
try:
    voltage = battery.read_battery_voltage()
    battery.blink_status()
    print(f"Battery voltage: {voltage:.2f}V")

    if voltage < battery.voltage_threshold:
        print("Low battery detected!")
        sleep()
except Exception as e:
    print(f"Error: {e}")

i2c = busio.I2C(scl=board.A1, sda=board.A0)
air = AHTx0(i2c_bus=i2c)

air_temp = air.temperature
air_humidity = air.relative_humidity

mox = Adafruit_BME680_I2C(i2c=i2c, debug=False)

start_time = time.monotonic()
warmup_duration = 120
while (time.monotonic() - start_time) < warmup_duration:
    print(f"Gas: {mox.gas} ohms")
    time.sleep(2)

coop_temp = mox.temperature
coop_humidity = mox.humidity
coop_gas = mox.gas
coop_pressure = mox.pressure

message: dict = {
    "device_id": os.getenv("DEVICE_ID", "unknown"),
    "api_key": os.getenv("API_KEY", "unknown"),
    "data": {
        "outside": {
            "air_temp": celsius_to_fahrenheit(air_temp),
            "humidity": air_humidity,
        },
        "coop": {
            "coop_temp": celsius_to_fahrenheit(coop_temp),
            "coop_humidity": coop_humidity,
            "coop_gas": coop_gas,
            "coop_pressure": coop_pressure,
        },
        "battery": voltage,
    },
}

sender = LoraSender("NULAYINN")

success = sender.send_data(message)

sleep()
