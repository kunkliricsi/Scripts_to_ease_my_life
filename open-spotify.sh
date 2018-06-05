#!/bin/bash

if ! pgrep -x "spotify" 2>/dev/null > /dev/null
then
	spotify 2>/dev/null > /dev/null &
	sleep 1
fi
dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.PlayPause 2>/dev/null > /dev/null
