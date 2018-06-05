# Scripts to ease my life
Generally, these are the scripts I wrote and use everyday to make my life a little less painful. Note that these scripts only work on Linux.

#### Spotify Opener
A bash script that opens Spotify if it's not open or acts as a traditional Play/Pause button if it's is.
I bound the script to the Audio Play/Pause button.

#### Adaptive Brightness Controller
A python script that lowers or increases the monitor's and laptop screen's brightnesses based on sunset and sunrise times. Useful if you like staying up late, but don't want to go blind by the age of 25. The script uses the [Astral](https://astral.readthedocs.io/en/latest/) module to determine sunset and sunrise times. To automate the process, I used cron with the following job that runs the script every 10 minutes from 3:00PM to 8:00AM: `*/10   0-7,15-23   *   *   *   /path/to/script/adaptive-brightness-controller.py`.
