#!/bin/bash

SCRIPT=$(readlink -f "$0")
BASEDIR=$(dirname "$SCRIPT")

ENABLED=$(cat "$BASEDIR"/enable-adaptive-brightness-controller)

export DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/1000/bus"

if [ $ENABLED -eq 1 ]
then
    su -c 'gdbus call --session --dest org.freedesktop.Notifications --object-path /org/freedesktop/Notifications --method org.freedesktop.Notifications.CloseNotification $(cat /tmp/last_id)' ricsi
    echo 0 > $BASEDIR/enable-adaptive-brightness-controller
    xrandr --output HDMI-1 --brightness 1
    cat /sys/class/backlight/intel_backlight/max_brightness > /sys/class/backlight/intel_backlight/brightness
    su -c 'gdbus call --session --dest org.freedesktop.Notifications --object-path /org/freedesktop/Notifications --method org.freedesktop.Notifications.Notify Brightness-Indicator 42 weather-clear "Adaptive Brightness: OFF" "" [] {} 20  | sed "s/[^ ]* //; s/,.//" > /tmp/last_id' ricsi

else
    su -c 'gdbus call --session --dest org.freedesktop.Notifications --object-path /org/freedesktop/Notifications --method org.freedesktop.Notifications.CloseNotification $(cat /tmp/last_id)' ricsi
    echo 1 > $BASEDIR/enable-adaptive-brightness-controller
    python3 $BASEDIR/adaptive-brightness-controller.py
    su -c 'gdbus call --session --dest org.freedesktop.Notifications --object-path /org/freedesktop/Notifications --method org.freedesktop.Notifications.Notify Brightness-Indicator 42 weather-clear-night "Adaptive Brightness: ON" "" [] {} 20  | sed "s/[^ ]* //; s/,.//" > /tmp/last_id' ricsi
fi