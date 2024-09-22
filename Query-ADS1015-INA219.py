#!/path/to/new/virtual/environment/bin/python3
import os
import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_ina219
# Prepare Raspberry Pi:
# apt install python
# apt install git
# git config --global user.name "John Doe"
# git config --global user.email johndoe@example.com
# git config --global init.defaultBranch main
# mkdir ~/.ssh
# cd ~/.ssh
# ssk-keygen -t ed25519
# <log into github and add public key>
# pip3 install --upgrade pip
# python3 -m venv /path/to/new/virtual/environment
# /path/to/new/virtual/environment/bin/pip3 install Adafruit-Blinka
# /path/to/new/virtual/environment/bin/pip3 install adafruit-circuitpython-ads1x15
# /path/to/new/virtual/environment/bin/pip3 install adafruit-circuitpython-ina219

# https://docs.circuitpython.org/projects/ads1x15/en/latest/api.html#adafruit_ads1x15.ads1015.ADS1015

class ads_object:
  def __init__(self, ads:ADS.ADS1015, positive_pin:int, negitive_pin:int, path:str|None=None):
    self.ads = ads
    self.gain = self.ads.gain
    self.out = ""
    self.file_path = ""
    self.positive_pin = positive_pin
    self.negitive_pin = negitive_pin
    if path is not None:
      self.file_path = path
    else:
      cwd = os.getcwd()
      self.file_path = f"{cwd}{os.pathsep}ads_out_{self.positive_pin}_{self.negitive_pin}.csv"
    self.channel=AnalogIn(ads, positive_pin, negitive_pin)
    data = f"time,voltage\n"
    with open(self.file_path, "w") as file:
      file.write(data)
  def write_to_file(self):
    data = f"{self.out}\n"
    with open(self.file_path, "a") as file:
      file.write(data)
  def create_output_string(self):
    ads_voltage = 0.0
    ads_voltage = self.channel.voltage
    # adc_value = chan_vcc.value
    time_in_ms = int(time.time() * 1000)
    self.out = f"{time_in_ms},{ads_voltage}"
  def display_on_screen(self):
      print(f"{self.out}")
  def get_next_sample(self):
    self.create_output_string()
    self.display_on_screen()
    self.write_to_file()

class ina_object:
  def __init__(self, ina:adafruit_ina219.INA219, path:str|None=None):
    self.ina = ina
    self.out = ""
    self.file_path = ""
    if path is not None:
      self.file_path = path
    else:
      cwd = os.getcwd()
      addr = self.ina.i2c_addr
      self.file_path = f"{cwd}{os.pathsep}ina_out_{addr}.csv"
    data = f"time,bus_voltage,shunt_voltage,current,power\n"
    with open(self.file_path, "w") as file:
      file.write(data)
  def write_to_file(self):
    data = f"{self.out}\n"
    with open(self.file_path, "a") as file:
      file.write(data)
  def create_output_string(self):
    bus_voltage = self.ina.bus_voltage
    shunt_voltage = self.ina.shunt_voltage
    current = self.ina.current
    power = self.ina.power
    time_in_ms = int(time.time() * 1000)
    self.out = f"{time_in_ms},{bus_voltage},{shunt_voltage},{current},{power}"
  def display_on_screen(self):
      print(f"{self.out}")
  def get_next_sample(self):
    self.create_output_string()
    self.display_on_screen()
    self.write_to_file()

i2c = busio.I2C(board.SCL, board.SDA)

object_array = []

# Use pin pairs A0+A1,A2+A3
# ADS Gain must literally be the value 2/3 to allow ~ 6volts
ads_5v = ADS.ADS1015(i2c, gain=2/3, address=72)
ads_object_5v = ads_object(ads_5v, ADS.P0, ADS.P1, path="./out_5v.csv")
object_array.append(ads_object_5v)

ads_3_3v = ADS.ADS1015(i2c, gain=1, address=72)
ads_object_3_3v = ads_object(ads_3_3v, ADS.P2, ADS.P3, path="./out_3_3v.csv")
object_array.append(ads_object_3_3v)

# Create the INA219 objects
# Addresses: Default = 0x40 = 64, A0 soldered = 0x41 = 65,
# A1 soldered = 0x44 = 68, A0 and A1 soldered = 0x45 = 69
ina219_1 = adafruit_ina219.INA219(i2c, addr=64)
ina219_object_1 = ina_object(ina219_1, "./out_ina219_1.csv")
object_array.append(ina219_object_1)

# ina219_2 = adafruit_ina219.INA219(i2c, addr=65)
# ina219_object_2 = ina_object(ina219_2, "./out_ina219_2.csv")
# object_array.append(ina219_object_2)
#
# ina219_3 = adafruit_ina219.INA219(i2c, addr=68)
# ina219_object_3 = ina_object(ina219_3, "./out_ina219_3.csv")
# object_array.append(ina219_object_3)

while True:
  for item in object_array:
    item.get_next_sample()

  time.sleep(.25)
