#!/usr/bin/env python3


import time

 from gpiozero import OutputDevice 


ON_THRESHOLD = 65 # (degrees Celcius) Fan kicks on at this temperature.
OFF_THRESHOLD = 55 # (degrees Celcius) Fan shuts off at this temparature.
SLEEP_INTERVAL = 5 # (seconds) How often we check the core temperature.
GPIO_PIN = 17 # Which GPIO pin you're usingto control the fan.


def get_temp():
    """Get the core temperature.
    
    Read file from /sys to get CPU temp in temp in C *1000
    
    Returns:
        int: The core temperature in thousandths of degrees Celcius.
    """
    with open('/sys/class/thermal_zone0/temp') as f:
        temp_str = f.read()

    try:
        return int(temp_str) / 1000
    except (IndexError, ValueError,) as e:
        raise RuntimeError('Could not parse temperature output.') from e

if __name__ == '__main__':
    # Validate the on and off thresholds
    if OFF_THRESHOLD > ON_THRESHOLD:
       raise RuntimeError('OFF_THRESHOLDS must be less than ON_THRESHOLD')


    fan = OutputDevice(GPIO_PIN)

    while True:
        temp = get_temp()

        # Start the fan if the temperature has reached the limit and the fan 
        # isn't already running.
        # NOTE: `fan.value` returns 1 for "on" and 0 for "off"
        if temp > ON_THRESHOLD and not fan.value:
            fan.on()

        # Stop the fan if the fan is running and the temperature has dropped 
        # to 10 degrees below the limit.
        elif fan.value and temp < OFF_THRESHOLD:
            fan.off()

        time.sleep(SLEEP_INTERVAL)