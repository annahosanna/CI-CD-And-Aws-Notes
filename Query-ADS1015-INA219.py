#!~/Desktop/python-venv/bin/python3
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

# Voltage regulator with .6 volt out per diode. (regardless of input voltage)
# R1 = 2200 ohms (or whatever it takes to get current in diode operating range)
# |--R1---|>|--|>|--|
# |     |           |
# *P0   Vout        |
# |     |           |
# Vcc   *P2         |
#       |           |
#       |--INA219---|--*P1--*P3--Gnd
#
# Voltage Divider Resistor Calculator
# https://www.ti.com/download/kbase/volt/volt_div3.htm#:~:text=Proble,or%20as%20few%20as%20one.
# R1 = 4700, R2 = 9100
# Vcc/P0
# |
# R1
# |
# |--Vout--INA219--|
# |                |
# R2               Rload/P2
# |                |
# |----------------|
# |
# Gnd/P1/P3
# Voltage Divder Current
# Itotal = Vin/(R1+R2)
# Current is the same across both resistors (Itotal)
# Next a load is connected in parallel to R2
# Use current divider formula for a parallel circuit
# Iload = Itotal * ((1/Rload)/((1/Rload)+(1/R2)))
# Vload = Iload * Rload
#
# Because Vload varies with Rload, calculating Vload is hard if you do not know Rload.
# So use gain

chan_vcc = AnalogIn(ads, ADS.P0, ADS.P1)
chan_vout = AnalogIn(ads, ADS.P2, ADS.P3)
chan_p0 = AnalogIn(ads, ADS.P0)
chan_p1 = AnalogIn(ads, ADS.P1)
chan_p2 = AnalogIn(ads, ADS.P2)
chan_p3 = AnalogIn(ads, ADS.P3)
# https://docs.circuitpython.org/projects/ina219/en/latest/api.html
# Create the INA219 object
ina219 = adafruit_ina219.INA219(i2c)

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
