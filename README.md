# Python-Passive-Infrared-Motion
Use a passive infrared detector to turn on an HDMI screen attached to a Raspberry Pi when movement is, or is not detected. The python script has two loops, one waits 5 minutes and checks to see if the screen is on, and if any movement has been detected in the last 5 minutes. If the screen is on, and no movement has been detected, it turns the screen off.

The second loop is threaded, and waits for the passive infrared detector to be triggered. It waits a tenth of a second and tests if the detector is still triggered to avoid being activated by power fluctuations and static electricity. It sets a variable that tells the first loop that movement has been detected. Then if the screen is off, it will turn it on.

Us the script https://gist.github.com/K7TRY/06624946653478dcd6c063b7f2d96ca5 to turn the HDMI on and off.
