Please run mainGame.py to play! Works better with headphones, though it still works
wihout.

MainGame.py imports all the other files: audioClass.py to record
and manage audio, classes.py which handles the onscreen moving parts, and fft.py which
uses the Cooley-Tukey FFT algorithm to make a frequency chart.

Currently, the recorder only takes a chunk of the audio to process with every onstep,
and the setup screen is very much a work in progress. (Highest and Lowest will set
the range the user is capable of singing) Also, transparent images will be a must.

The parts with the most algorithmic complexity are the FFT algorithm and decoding its
output into usable frequency data by extracting the important peaks. Run the audioPlayTest.py
and audioRecordTest.py files for a demos with real numbers.
