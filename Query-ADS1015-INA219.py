#!/usr/bin/python3
import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_ina219

# Notes:
# Circuit example which combines the two to measure volatage and current
# https://www.instructables.com/Arduino-Voltage-and-Current-Measurement-ACS712-ADS/

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# https://docs.circuitpython.org/projects/ads1x15/en/latest/api.html#adafruit_ads1x15.ads1015.ADS1015
# Review constructor options: mode might need to be zero - Use circuit to test for 1 shot vs. continious.
# You can also set a sample rate - does a higher sample rate take more power from pi?
#
# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c)

# AnalogIn(ads: ADS1x15, positive_pin: int, negative_pin: int | None = None)
# Integer constants are: ADS.P0, ADS.P1, ADS.P2, ADS.P3
# Note: P0 - P3 are Vin, gnd is shared with ADC.
# !! So when your testing this, your 3.3 volt and 5 volt pins which you want to measure must share a common ground !!

# A simple volatage divider should work:
  # Vin = 5
  # Vout = 3.3
  # Selecting correct value resistors important to current
  # https://www.ti.com/download/kbase/volt/volt_div3.htm#:~:text=Problem:,or%20as%20few%20as%20one.
  # E24 = 5% resistor rating
  # Best values are R1 = 4.7K; R2 = 9.1K
#
# |----|--Rvar--|
# |    |        |
# |    |        R2
# |    |        |
# |    |        *--P0
# |    /        |
# |    |        INA219
# |    R3       |
# Vcc  |        -----*--P2
# |    |        |
# |    |        R1
# |    |        |
# |----|-----|--|----*--P3
#            |
#            |--*--P1
# Vcc = 9v battery + 7805
# R3 creates a current divider with resistance = R1 + R2
# R2 + R1 used to create a 3.3 volt volage divider
# Place INA219 behind a resistor
# '*' are sample points for 5 and 3.3 volts ADS1015
# Put current sensor in series
# Rvar controls volage divider (should be 0 ohm normally)
# R1 = 4700 ohm, R2 = 9100 ohm, R3 = 13800 ohm + on/off switch
# Sample ground to get realitive voltage, as it may float


# Create single-ended input on channel 0
chan_5v = AnalogIn(ads, ADS.P0, ADS.P1)
chan_3_3v = AnalogIn(ads, ADS.P2, ADS.P3)
# Optionally this can take two arguments if for instance you wanted to Latch at a particular voltage differential

# https://docs.circuitpython.org/projects/ina219/en/latest/api.html
# Create the INA219 object
ina219 = adafruit_ina219.INA219(i2c)

while True:
    # Read the ADC value from ADS1015

    # voltage is a float
    adc_voltage_5v = chan_5v.voltage
    # This is 12 bit ADC, but the value will be put in a 16 bit int
    adc_value_5v = chan_5v.value

    # voltage is a float
    adc_voltage_3_3v = chan_3_3v.voltage
    # This is 12 bit ADC, but the value will be put in a 16 bit int
    adc_value_3_3v = chan_3_3v.value


    # Read the INA219 values for current
    bus_voltage = ina219.bus_voltage
    shunt_voltage = ina219.shunt_voltage
    current = ina219.current
    power = ina219.power


    # Print the results
    print("--------------------")
    # ADS1015
    print("ADC 5v Voltage: {:.2f}V".format(adc_voltage_5v))
    print("ADC 5v Value: {}".format(adc_value_5v))
    print("ADC 3.3v Voltage: {:.2f}V".format(adc_voltage_3_3v))
    print("ADC 3.3v Value: {}".format(adc_value_3_3v))

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
