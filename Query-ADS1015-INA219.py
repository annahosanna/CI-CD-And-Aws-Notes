#!/path/to/new/virtual/environment/bin/python3
import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_ina219

# Prepare Raspberry Pi:
# apt install python
# apt install git
# pip3 install --upgrade pip
# python3 -m venv /path/to/new/virtual/environment
# /path/to/new/virtual/environment/bin/pip3 install Adafruit-Blinka
# /path/to/new/virtual/environment/bin/pip3 install adafruit-circuitpython-ads1x15
# /path/to/new/virtual/environment/bin/pip3 install adafruit-circuitpython-ina219

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)
# https://docs.circuitpython.org/projects/ads1x15/en/latest/api.html#adafruit_ads1x15.ads1015.ADS1015
# Constructor
# adafruit_ads1x15.ads1015.ADS1015(
#   i2c: I2C,
#   gain: float = 1,
#   data_rate: int | None = None,
#   mode: int = 256,
#   comparator_queue_length: int = 0,
#   comparator_low_threshold: int = -32768,
#   comparator_high_threshold: int = 32767,
#   comparator_mode: int = 0,
#   comparator_polarity: int = 0,
#   comparator_latch: int = 0,
#   address: int = 72)
#
# Create the ADC object using the I2C bus
# Set gain to shrink 5v -> 3v3
gain = 0.66
# Pass by parameter name, except it does not seem to be duck typing i2c yet
# so pass it positionally
ads = ADS.ADS1015(i2c, gain=gain)
# Pass by first position
# ads = ADS.ADS1015(i2c)

# Place INA219, in series
# '*' are sample points for vcc and vout ADS1015
# Sample ground to get realitive voltage, as it may float
# Each sample point may only be used for one constructor
# The FlatStat will not share a common ground, so take the voltage difference
# Voltage regulator with .6 volt out per diode. (regardless of input voltage)
# R1 = 2200 ohms (or whatever it takes to get current in diode operating range)
# Voltage Divider Resistor Calculator
# https://www.ti.com/download/kbase/volt/volt_div3.htm#:~:text=Proble,or%20as%20few%20as%20one.
# R1 = 4700, R2 = 9100?
# Voltage Divder Current
# Itotal = Vin/(R1+R2)
# Current is the same across both resistors (Itotal)
# Next a load is connected in parallel to R2
# Use current divider formula for a parallel circuit
# Iload = Itotal * ((1/Rload)/((1/Rload)+(1/R2)))
# Vload = Iload * Rload
# Because Vload varies with Rload, calculating Vload is hard if you do not know Rload.
# So use gain
# watts = V*I = I*I*R
# R = V/I
# 5v @ .25 watt; W/V = I; W/(I*I) = R; R = (W/1)/((W/V)*(W/V)) = W/1*V/W*V/W = V*V/W
# So in order not to cook my resistor R >= 100
# Assignment:
# Measure flat sat raw battery voltage
# Mesure flat sat EPS battery current
# Measurement must be able to be bi-directional
# Measure 5v and 3.3v supplies
# Interface via H1/H2 connector
# Isolate measurement using 2 KOhm to 10 KOhm
# Note: pins cannot supply more than 2 mA, so target 1.25 mA
#   V = I * R --> V/I = R
#   3.3/0.00125 = 2.640 KOhm
#   5/0.00125 = 4.000 KOhm
# 4 or more samples per second
# Store values with a time tag to in a CSV file
#   time, input, type, value (or multiple files)
# Should provide an LED that a measured voltage is present
# Should Display values to the screen
# Build in KiCAD or some other way to show Dave design.
#
# Bridge Circuit almost (must have diodes, otherwise equal R1 will cancel out)
# INA219 can only measure positive voltage up to 29v
# 2200 ohm resistors
# |---Vcc/Gnd----R1--|<|--|
# R1                      |
# |----Vout--INA219-------|
# R1                      |
# |---Gnd/Vcc----R1--|<|--|
#
#
# ADC1015 can measure positive or negitive voltage up to 4v
# Probably can just put in a resistor before the point you are sampling
# 4700 Ohm
#
# f.close in finally
# f = open('workfile', 'w', encoding="utf-8")
# "a" if file already exists and you do not want to overwrite it
# try:
#    TARGET = value
#    SUITE
#except:
#    hit_except = True
#    if not exit(manager, *sys.exc_info()):
#        raise
#finally:
#    if not hit_except:
#        exit(manager, None, None, None)
# file_path = "example.txt"
# if os.path.exists(file_path):
#    print(f"File {file_path} already exists.")
#else:
#    print(f"File {file_path} does not exist. Creating it.")
# Write data to the file
#data = "This is some example data to write to the file."
#with open(file_path, "w") as file:
#    file.write(data)
# # Function to get current timestamp in milliseconds
# def get_timestamp_ms():
#     return int(time.time() * 1000)

# Write timestamps to the file
# with open(timestamp_file, "w") as file:
#     for _ in range(10):  # Write 10 timestamps as an example
#         timestamp = get_timestamp_ms()
#         file.write(f"{timestamp}\n")
#         time.sleep(0.1)  # Wait 100ms between timestamps
#print(f"Timestamps have been written to {timestamp_file}.")
# print(f"Data has been written to {file_path}.")
# class Example:
#     def __init__(self):
#         self.value = 0

#     def increment(self):
#         self.value += 1

#     def get_value(self):
#         return self.value

# # Usage
# obj = Example()
# obj.increment()
# print(obj.get_value())
#
# Create an array with multiple types of objects
# mixed_array = [42, "Hello", 3.14, True, [1, 2, 3], {"name": "John", "age": 30}]

# # Iterate over the array
# for item in mixed_array:
#     print(f"Type: {type(item)}, Value: {item}")
# # Initialize an empty array
# my_array = []

# # Append data to the array using the append() method
# my_array.append(42)
# my_array.append("Hello")
# my_array.append([1, 2, 3])

# # Alternatively, use the extend() method to append multiple items at once
# my_array.extend([4, 5, 6])

# # Print the updated array
# print(my_array)
chan_vcc = AnalogIn(ads, ADS.P0, ADS.P1)
chan_vout = AnalogIn(ads, ADS.P2, ADS.P3)
chan_p0 = AnalogIn(ads, ADS.P0)
chan_p1 = AnalogIn(ads, ADS.P1)
chan_p2 = AnalogIn(ads, ADS.P2)
chan_p3 = AnalogIn(ads, ADS.P3)
# https://docs.circuitpython.org/projects/ina219/en/latest/api.html
# Create the INA219 object
ina219 = adafruit_ina219.INA219(i2c)

# Try:
#   Open files
#   create array of channel objects
#   While
#     foreach object in objects
#       out = object.get_string(channel)
#       write(file,string)
# Except:
#   print "panic"
# Finally:
#   foreach obect in objects
#     object.closefile()
#
# class ExampleClass:
#     def __init__(self):
#         print("Constructor called")
#         raise Exception("Exception raised in constructor")

#     def __del__(self):
#         print("Destructor called")
#         raise Exception("Exception raised in destructor")

# try:
#     obj = ExampleClass()
# except Exception as e:
#     print(f"Caught exception: {e}")

# # The destructor will be called when the object goes out of scope
# # or when it's explicitly deleted
# del obj
# Use pin pairs A0+A1,A2+A3
# Gain can be 2/3 to allow ~ 6volts
while True:
    # Read the ADC value from ADS1015

    # voltage is a float
    adc_voltage_vcc = chan_vcc.voltage
    # This is 12 bit ADC, but the value will be put in a 16 bit int
    adc_value_vcc = chan_vcc.value

    adc_voltage_vout = chan_vout.voltage
    adc_value_vout = chan_vout.value

    adc_voltage_p0 = chan_p0.voltage
    adc_value_p0 = chan_p0.value

    adc_voltage_p1 = chan_p1.voltage
    adc_value_p1 = chan_p1.value

    adc_voltage_p2 = chan_p2.voltage
    adc_value_p2 = chan_p2.value

    adc_voltage_p3 = chan_p3.voltage
    adc_value_p3 = chan_p3.value


    # Read the INA219 values for current
    bus_voltage = ina219.bus_voltage
    shunt_voltage = ina219.shunt_voltage
    current = ina219.current
    power = ina219.power


    # Print the results
    print("--------------------")
    # ADS1015
    print("ADC Vcc Voltage: {:.2f}V".format(adc_voltage_vcc))
    print("ADC Vcc Value: {}".format(adc_value_vcc))

    print("ADC Vout Voltage: {:.2f}V".format(adc_voltage_vout))
    print("ADC Vout Value: {}".format(adc_value_vout))

    print("ADC Channel P0 Voltage: {:.2f}V".format(adc_voltage_p0))
    print("ADC Channel P0 Value: {}".format(adc_value_p0))

    print("ADC Channel P0 Voltage: {:.2f}V".format(adc_voltage_p1))
    print("ADC Channel P0 Value: {}".format(adc_value_p1))

    print("ADC Channel P0 Voltage: {:.2f}V".format(adc_voltage_p2))
    print("ADC Channel P0 Value: {}".format(adc_value_p2))

    print("ADC Channel P0 Voltage: {:.2f}V".format(adc_voltage_p3))
    print("ADC Channel P0 Value: {}".format(adc_value_p3))

    print("--------------------")

    # INA219
    print("INA219 Bus Voltage: {:.2f}V".format(bus_voltage))
    print("INA219 Shunt Voltage: {:.2f}mV".format(shunt_voltage * 1000))
    print("INA219 Current: {:.2f}mA".format(current))
    print("INA219 Power: {:.2f}mW".format(power))

    print("--------------------")
    # End with a blank line to seperate samples
    print("")

    # Wait for 1 second before the next reading
    time.sleep(1)
