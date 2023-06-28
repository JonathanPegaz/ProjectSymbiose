
import bluetooth
import struct
import time
from ble_advertising import advertising_payload
from ble_uart_peripheral import *
from time import sleep_ms
from machine import Pin, SPI
from mfrc522 import *

ble = bluetooth.BLE()
uart = BLEUART(ble, "esp2")

sck = Pin(18, Pin.OUT)
mosi = Pin(23, Pin.OUT)
miso = Pin(19, Pin.OUT)
spi = SPI(baudrate=100000, polarity=0, phase=0, sck=sck, mosi=mosi, miso=miso)

sda1 = Pin(5, Pin.OUT)
sda2 = Pin(4, Pin.OUT)
sda3 = Pin(2, Pin.OUT)

def on_rx():
    received = uart.read().decode().strip()
    if received == "test":
        Pin(26, mode=Pin.OUT, value=1)
        print("test d'amour : ", received)
    else:
        print("rx: ", received)

uart.irq(handler=on_rx)
nums = [4, 8, 15, 16, 23, 42]
i = 0

try:
    while True:
        rdr1 = MFRC522(spi, sda1)
        rdr2 = MFRC522(spi, sda2)
        rdr3 = MFRC522(spi, sda3)
        
        (stat, tag_type) = rdr1.request(rdr1.REQIDL)
        if stat == rdr1.OK:
            (stat, raw_uid) = rdr1.anticoll()
            if stat == rdr1.OK:
                uid = ("0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                uart.write("rfid1")
                print("rfid1")
        
        (stat, tag_type) = rdr2.request(rdr2.REQIDL)
        if stat == rdr2.OK:
            (stat, raw_uid) = rdr2.anticoll()
            if stat == rdr2.OK:
                uid = ("0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                uart.write("rfid2")
                print("rfid2")
        
        (stat, tag_type) = rdr3.request(rdr3.REQIDL)
        if stat == rdr3.OK:
            (stat, raw_uid) = rdr3.anticoll()
            if stat == rdr3.OK:
                uid = ("0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                uart.write("rfid3")
                print("rfid3")
 
        time.sleep_ms(1000)
except KeyboardInterrupt:
    pass

uart.close()

  