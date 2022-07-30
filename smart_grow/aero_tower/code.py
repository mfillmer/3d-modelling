import time
import board
from digitalio import DigitalInOut, Direction

led = DigitalInOut(board.LED_INVERTED)
led.direction = Direction.OUTPUT

pump = DigitalInOut(board.D9)
pump.direction = Direction.OUTPUT
pump_pause = 7*60
pump_interval = 20
pulse_intensity = 0.0005

while True:
    led.value = False
    t_end = time.monotonic() + pump_interval

    while time.monotonic() < t_end:
        pump.value = True
        time.sleep(pulse_intensity)
        pump.value = False
        time.sleep(pulse_intensity)

    led.value = True
    time.sleep(pump_pause)
