import RPi.GPIO as GPIO

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Get all available GPIO pins
available_pins = [2, 3, 4, 17, 27, 22, 10, 9, 11, 5, 6, 13, 19, 26, 14, 15, 18, 23, 24, 25, 8, 7, 12, 16, 20, 21]

# Function to query pin status
def query_pin(pin):
  GPIO.setup(pin, GPIO.IN)
  state = GPIO.input(pin)
  return f"GPIO {pin}: {'HIGH' if state else 'LOW'}"

# Query all available pins
for pin in available_pins:
  print(query_pin(pin))

# Clean up GPIO
GPIO.cleanup()
