import board
import busio
import digitalio
import msgpack
from io import BytesIO

import adafruit_rfm9x


def default(obj) -> dict:
    if isinstance(obj, bytes):
        return {"__bytes__": True, "data": list(obj)}
    raise TypeError(f"Object of type {type(obj)} is not msgpack serializable")

class LoraSender:
    def __init__(self, device_id: str, frequency: int = 915):
        """
        Initialize LoRa sender with unique ID

        :param device_id: Unique identifier for this sender
        :param frequency: Frequency in MHz
        """
        self.device_id = device_id

        spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
        cs = digitalio.DigitalInOut(board.RFM_CS)
        reset = digitalio.DigitalInOut(board.RFM_RST)

        self.rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, frequency)
        self.rfm9x.tx_power = 23
        self.rfm9x.spreading_factor = 7
        self.rfm9x.signal_bandwidth = 125000
        self.rfm9x.coding_rate = 5
        self.rfm9x.enable_crc = True
        self.rfm9x.ack_retries = 3
        self.rfm9x.ack_wait = 0.7

    def send_data(self, data: dict) -> bool:
        """
        Send data with device ID
        :param data: Sensor data dict
        :return: bool
        """
        data_packet = {
            'sender_id': self.device_id,
            'data': data
        }
        try:
            buffer = BytesIO()
            msgpack.pack(data_packet, stream=buffer)
            packed_data = buffer.getvalue()
            ack = self.rfm9x.send_with_ack(packed_data)
            return ack
        except Exception as er:
            print(f"Error sending data: {er}")
            return False

