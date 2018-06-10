# Scripts to ease my life
Generally, these are the scripts I wrote and use everyday to make my life a little less painful. Note that these scripts only work on Linux.

#### Spotify Opener
A bash script that opens Spotify if it's not open or acts as a traditional Play/Pause button if it's is.
I bound the script to the Audio Play/Pause button.

#### Adaptive Brightness Controller
A python script that lowers or increases the screen brightness based on sunset, dusk, dawn and sunrise times. Useful if you like staying up late, but don't want to go blind by the age of 25. The script uses the [Astral](https://astral.readthedocs.io/en/latest/) module to determine the needed times. To automate the process, I used cron with the following job that runs the script every minute from 4:00PM to 8:00AM: `*	 0-7,16-23	 *	 *	 *	 /path/to/script/adaptive-brightness-controller.py`.<br>
<br>I wrote a shell script to enable or disable this function, which also sends a notification to see if the adaptive brightness is on or not.
