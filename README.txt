
In Tweater, use your pitch! Sing high and low to help Burdy catch all the bugs before they starve.

Please run runFullGame.py to play! Works better with headphones, though it still works
wihout.

runFullGame.py imports all the other files including audioClass.py to record
and manage audio, fft.py which uses the Cooley-Tukey FFT algorithm to make a frequency chart
and all the different screens.

Start the game and select the mode you would like to play. Easy, medium, and hard just 
ramp up the speed of your gameplay. Infinite mode is the best way to chill and have fun
screaming at the bird. If you want to be more classy, sing a sample song on singing mode
that maps a real scale starting from G3. Next, do some setup. Run the noise calculation
if you're in a noisy place so the game won't pick it up. Record the highest and lowest
notes you can (or are willing to) sing/scream for the game. (This will only affect
the range outside of singing mode.) Now you're ready to start.

Careful! Don't eat the nasty red bugs, and make sure to get those green ones for bonus
points and lives. The game speeds up as you play and eat, but slows down if you miss a bug.

The time of day changes according to the amount of
stars created from a 'star generation' engine, based on a modified version of Conway's
Game of Life. The seeds of the 'star generation' are placed depending on the loudness of 
your sound along with the pitch, so watch the stars interact and evolve as you scream louder,
which in turn triggers the sky to change.