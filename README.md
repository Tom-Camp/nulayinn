# NuLay Inn

The NuLay Inn is a sensor package for monitoring the environment in our chicken coop. It is designed to be used with 
the Adafruit Feather RP2040 RFM95, an Adafruit BME680 - Temperature, Humidity, Pressure and Gas Sensor, and an Adafruit 
AHT20 - Temperature & Humidity Sensor Breakout Board.

The name NuLay Inn is a nod to the historic [NuWray Hotel](https://www.nuwray.com/) here in Burnsville, North Carolina.

## Features

The system is designed to run with a battery and solar panel, and is capable of sending data to a server via LoRa. 
The data is then sent to an API server for storage and analysis. The system is designed to be low power, with a sleep 
mode that sends data every hour. The AHT20 sensor is used for temperature and humidity outside the coop, while the 
BME680 sensor is for temperature, humidity, pressure and gas inside the coop.

The code includes a power management system that monitors the battery voltage and puts the system to sleep if the 
voltage drops below a certain threshold to prevent malformed packets. The system wakes up every hour to take a reading 
and sends the data to a [Raspberry Pi RFM9x receiver](https://github.com/Tom-Camp/rfm_receiver). The receiver then relays 
the data to an API server.

## Hardware

- [Adafruit Feather RP2040 RFM95](https://www.adafruit.com/product/5714)
- [Adafruit BME680 - Temperature, Humidity, Pressure and Gas Sensor](https://www.adafruit.com/product/3660)
- [Adafruit AHT20 - Temperature & Humidity Sensor Breakout Board](https://www.adafruit.com/product/4566)
- [Lithium Ion Battery - 3.7V 2000mAh](https://www.digikey.com/en/products/detail/adafruit-industries-llc/2011/6612469?so=89389693&content=productdetail_US&mkt_tok=MDI4LVNYSy01MDcAAAGWajcL_5vQOjPWD-eAVw-kvba4MqUPiOxf-pwP6LgDc1mBYv5LtwWUqilrqSwNAF13SQ-5bRaKJfkmGwpMcVgywjLbSSO0idYhVo5vVjcd)
- Solar Panel with 5V 3.5W Continuously Charging

The [diagram](diagram) file describes the additions to the board needed for the battery monitor to work. Connect a 100kΩ 
resistor to the VBAT pin and a 100kΩ resistor to a ground pin with a jumper wire connected in between the two resistors 
going to one of the analog pins (A0, A1, A2, A3) to form a voltage divider. If you choose an analog pin other than A3, 
you will need to change the `battery_pin` value in line 9 of the [battery_monitor.py](lib/battery_monitor.py) file.

[Adafruit Feather RP2040 RFM95 pinout](https://cdn-learn.adafruit.com/assets/assets/000/120/283/original/adafruit_products_Adafruit_Feather_RP2040_RFM95_Pinout.png?1681763258)

## Software

The software is written in CircuitPython 9.x and is designed to run on the Adafruit Feather RP2040 RFM95. The code uses
the following Adafruit libraries included in the [Adafruit CircuitPython Library Bundle](https://docs.circuitpython.org/projects/bundle/en/latest/) 
but not included in this repository:

- adafruit_bus_device
- adafruit_ahtx0
- adafruit_bme680
- adafruit_rfm9x
