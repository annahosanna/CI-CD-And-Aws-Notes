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
# chmod 700 ~/.ssh
# chmod 644 ~/.ssh/id_ed25519.pub
# chmod 600 ~/.ssh/id_ed25519
#
# <log into github and add public key>
#
# pip3 install --upgrade pip
# python3 -m venv /path/to/new/virtual/environment
# /path/to/new/virtual/environment/bin/pip3 install Adafruit-Blinka
# /path/to/new/virtual/environment/bin/pip3 install adafruit-circuitpython-ads1x15
# /path/to/new/virtual/environment/bin/pip3 install adafruit-circuitpython-ina219

# Documentation:
# https://docs.circuitpython.org/projects/ads1x15/en/stable/
# https://docs.circuitpython.org/projects/ina219/en/stable/

# Basic formulas:
# Watts = V*I = I^2 * R = V^2/R
# R = V * I/I^2 = V/I = V^2/Watts = Watts/I^2
# V = I*R = Watts/I
# I = V/R = Watts/V

# From this: A quater watt resistor at 5 volts must have a resistance of at least 100 ohm
# However:
# Based on GPIO limitations per pin:
# 3.3v * .017 amps = .0561 watts max per pin max. Min R equals about 200 ohm
# 5v * .01122 amps =.0561 watts. Min R equals about 450 ohm

# This has a bug in that it doesn't try to parse a file path for directory information
# filepath = "/home/user/documents/example.txt"

# Get the directory name
# dirname = os.path.dirname(filepath)
# print(dirname)

# # Get the base filename
dirname, filename = os.path.split("")
# basename = os.path.basename(filepath)
# print(basename)
#
# Base name should include full path and extra info
class find_unique_filename:
  """Class to create a unique filename"""
  def __init__(self, base_name:str="__",suffix:str=""):
    self.base_path = ""
    self.base_name = ""
    self.base_path, self.base_name = os.path.split(base_name)
    self.file_path = ""
    self.temp_path = ""
    self.file_increment = 0
    self.suffix=suffix
    if self.base_path is "" or self.base_path is None or not os.path.isdir(self.base_path):
      self.base_path = f"{os.getcwd()}{os.pathsep}"
    self.temp_path = f"{self.base_path}{self.base_name}{self.suffix}"
  def getname(self):
    """Build the filename and return it"""
    while os.path.exists(self.temp_path):
      self.temp_path = f"{self.base_path}{self.base_name}_{self.file_increment}{self.suffix}"
      self.file_increment = self.file_increment + 1
    self.file_path = self.temp_path
    return self.file_path

class ads_object:
  """Class responsible for querying the ADS and then writing data to a file and the screen."""
  def __init__(self, ads:ADS.ADS1015, positive_pin:int, negitive_pin:int, base_name:str="_"):
    self.ads = ads
    self.out = ""
    self.file_path = ""
    self.positive_pin = positive_pin
    self.negitive_pin = negitive_pin
    self.base_name = base_name
    unique_name=find_unique_filename(base_name=f"{self.base_name}_ads_out_{self.positive_pin}_{self.negitive_pin}",suffix=".csv")
    self.file_path=unique_name.getname()
    self.channel=AnalogIn(ads, positive_pin, negitive_pin)
    data = f"\"time_in_ms\",\"voltage\"\n"
    with open(self.file_path, "w") as file:
      file.write(data)
    self.start_time = int(time.time() * 1000)
  def write_to_file(self):
    data = f"{self.out}\n"
    with open(self.file_path, "a") as file:
      file.write(data)
  def create_output_string(self):
    ads_voltage = 0.0
    ads_voltage = self.channel.voltage
    # adc_value = chan_vcc.value
    time_in_ms = int(time.time() * 1000) - self.start_time
    self.out = f"{time_in_ms},{ads_voltage}"
  def display_on_screen(self):
    print(f"{self.out}")
  def get_next_sample(self):
    """Method responsible for querying the ADS and displaying the output"""
    self.create_output_string()
    self.display_on_screen()
    self.write_to_file()

class ina_object:
  """Class responsible for querying the INA and then writing data to a file and the screen."""
  def __init__(self, ina:adafruit_ina219.INA219, base_name:str="_"):
    self.ina = ina
    self.out = ""
    self.file_path = ""
    self.base_name=base_name
    addr = self.ina.i2c_addr
    unique_name=find_unique_filename(base_name=f"{self.base_name}_{addr}",suffix=".csv")
    self.file_path=unique_name.getname()
    data = f"\"time_in_ms\",\"bus_voltage\",\"shunt_voltage\",\"current,power\"\n"
    with open(self.file_path, "w") as file:
      file.write(data)
    self.start_time = int(time.time() * 1000)
  def write_to_file(self):
    data = f"{self.out}\n"
    with open(self.file_path, "a") as file:
      file.write(data)
  def create_output_string(self):
    bus_voltage = self.ina.bus_voltage
    shunt_voltage = self.ina.shunt_voltage
    current = self.ina.current
    power = self.ina.power
    time_in_ms = int(time.time() * 1000) - self.start_time
    self.out = f"{time_in_ms},{bus_voltage},{shunt_voltage},{current},{power}"
  def display_on_screen(self):
    print(f"{self.out}")
  def get_next_sample(self):
    """Method responsible for querying the INA and displaying the output"""
    self.create_output_string()
    self.display_on_screen()
    self.write_to_file()

i2c = busio.I2C(board.SCL, board.SDA)

object_array = []

# Use pin pairs A0+A1,A2+A3
# ADS Gain must literally be the value 2/3 to allow ~ 6volts
ads_5v = ADS.ADS1015(i2c, gain=2/3, address=72)
ads_object_5v = ads_object(ads_5v, ADS.P0, ADS.P1, base_name="out_5v")
object_array.append(ads_object_5v)

ads_3_3v = ADS.ADS1015(i2c, gain=1, address=72)
ads_object_3_3v = ads_object(ads_3_3v, ADS.P2, ADS.P3, base_name="out_3_3v")
object_array.append(ads_object_3_3v)

# Create the INA219 objects
# Addresses: Default = 0x40 = 64, A0 soldered = 0x41 = 65,
# A1 soldered = 0x44 = 68, A0 and A1 soldered = 0x45 = 69
ina219_1 = adafruit_ina219.INA219(i2c, addr=64)
ina219_object_1 = ina_object(ina219_1, "out_ina219_1")
object_array.append(ina219_object_1)

# ina219_2 = adafruit_ina219.INA219(i2c, addr=65)
# ina219_object_2 = ina_object(ina219_2, "out_ina219_2")
# object_array.append(ina219_object_2)
#
# ina219_3 = adafruit_ina219.INA219(i2c, addr=68)
# ina219_object_3 = ina_object(ina219_3, "out_ina219_3")
# object_array.append(ina219_object_3)

while True:
  for item in object_array:
    item.get_next_sample()
  time.sleep(0.25)
