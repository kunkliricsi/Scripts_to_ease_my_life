#!/bin/bash

ENABLED="$(cat /usr/local/etc/enable-adaptive-brightness-controller)"

if [ $ENABLED -eq 1 ]
then
    echo 0 > /usr/local/etc/enable-adaptive-brightness-controller
    xrandr --output HDMI-1 --brightness 1
    cat /sys/class/backlight/intel_backlight/max_brightness > /sys/class/backlight/intel_backlight/brightness
    xset -led 2 led off
else
    echo 1 > /usr/local/etc/enable-adaptive-brightness-controller
    python3 /usr/local/bin/adaptive-brightness/adaptive-brightness-controller.py
    xset -led 2 led on
fi