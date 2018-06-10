#!/usr/bin/python3

import inspect, os
import pytz
import sys
from subprocess import Popen, check_output
from math import pi, cos
from datetime import timezone, datetime, timedelta
from astral import Astral

# Gettings scripts directory
BASEDIR = os.path.dirname(os.path.realpath(sys.argv[0]))

# Checking if adaptive brightness is enabled
enabled_file = '%s/enable-adaptive-brightness-controller' % BASEDIR
enabled = int(check_output(['cat', enabled_file]).decode('utf-8'))

if (enabled == 0):
    sys.exit()

# Settings up astral to get correct dawn and dusk times.
#       civil:          6 degrees
#       nautical:       12 degrees
#       astronomical:   18 degrees
a = Astral()
a.solar_depression = 'astronomical'

# Initializing current location to determine correct date values.
city_name = 'Budapest'
city = a[city_name]

# Settings up sun object with initialized values.
today = datetime.today()
sun = city.sun(date = today, local = True)

# Getting datetimes of sunset, sunrise, dusk and dawn with sun object.
# Initializing now datetime with correct timezone tag.
sunset = sun['sunset']
dusk = sun['dusk']
sunrise = sun['sunrise']
dawn = sun['dawn']
now = datetime.now(pytz.timezone(city.timezone))

# Getting maximum brightness values
max_gamma = 1
max_brightness_file = '/sys/class/backlight/intel_backlight/max_brightness'
max_brightness = int(check_output(['cat', max_brightness_file]).decode('utf-8'))

# Setting up minimum brightness values.
min_gamma = 0.3
min_brightness = 0.09

# gamma is the value that will get inserted into the xrandr command
# brightness is the value which will get echod into the /sys/.../brightness
gamma = None
brightness = None

if (now > sunrise and now < sunset):
    gamma = max_gamma
    brightness = max_brightness

elif (now > dusk or now < dawn):
    gamma = min_gamma
    brightness = int(min_brightness * max_brightness)

else:

    if (now <= sunrise):
        time_between = sunrise - dawn
        elapsed = now - dawn
    
    elif (now >= sunset):
        time_between = dusk - sunset
        elapsed = dusk - now

    gamma = elapsed.seconds*(1 - min_gamma) / time_between.seconds + min_gamma
    brightness = int(max_brightness * (elapsed.seconds*(1 - min_brightness) / time_between.seconds + min_brightness))

# Sending out cat command to set laptop monitor's brightness
command = ('echo %d > /sys/class/backlight/intel_backlight/brightness' % brightness)
Popen(['bash', '-c', command])

# Sending out xrandr command to set monitor's brightness.
command = ('xrandr --output HDMI-1 --brightness %f' % gamma)
Popen(['su', '-c', command, 'ricsi'])