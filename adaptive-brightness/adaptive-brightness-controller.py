#!/usr/bin/python3

import pytz
import sys
from subprocess import Popen, call, check_output
from math import pi, cos
from datetime import timezone, datetime, timedelta
from astral import Astral

# Checking if adaptive brightness is enabled
enabled_file = '/usr/local/etc/enable-adaptive-brightness-controller'
enabled = int(check_output(['cat', enabled_file]).decode('utf-8'))

if (enabled == 0):
    sys.exit()

# Initializing current location to determine correct date values.
a = Astral()
a.solar_depression = 'civil'

city_name = 'Budapest'
city = a[city_name]

today = datetime.today()
sun = city.sun(date = today, local = True)

# Getting datetimes of sunset and sunrise +- 15 minutes
# and initializing now datetime with correct timezone tag.
# Some adjustments to sunset/sunrise times may be needed.
sunset = sun['sunset'] - timedelta(minutes = 30)
sunrise = sun['sunrise'] + timedelta(minutes = 30)
now = datetime.now(pytz.timezone(city.timezone))

# Initializing the two midnight points.
midnight_0 = now.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
midnight_24 = midnight_0 + timedelta(days = 1)

# Calculating elapsed time between midnight and sunrise/sunset.
morning = sunrise - midnight_0
evening = midnight_24 - sunset

# A value between 0 and 1. Calculated by the cosine of now and sunrise or sunset.
# It will be used to determine the screen brightness value.
gamma = None

if now <= sunrise:
    # Calculating the screen brightness with cos(x + pi).
    elapsed = now - midnight_0
    gamma = (cos(float(elapsed.seconds/morning.seconds) * pi + pi) + 1) * 0.5

elif now >= sunset:
    # Calculating the screen brightness with cos(x).
    elapsed = midnight_24 - now
    gamma = (cos(float(elapsed.seconds/morning.seconds) * pi + pi) + 1) * 0.5

else:
    # There is nothing to do, exiting...
    sys.exit()

# Getting first screen's max brightness.
max_brightness_file = '/sys/class/backlight/intel_backlight/max_brightness'
max_brightness = int(check_output(['cat', max_brightness_file]).decode('utf-8'))

# Calculating the brightness to send to the first monitor
brightness = int(max_brightness * gamma)

# Setting minimum brightness values
gamma += 0.3
if gamma > 1.0:
    gamma = 1.0

if brightness < 300:
    brightness = 300

# Sending out cat command to set laptop monitor's brightness
command = ('echo %d > /sys/class/backlight/intel_backlight/brightness' % brightness)
Popen(['sudo', 'bash', '-c', command])

# Sending out xrandr command to set monitor's brightness.
command = ('xrandr --output HDMI-1 --brightness %f' % gamma)
Popen(['su', '-c', command, 'ricsi'])
