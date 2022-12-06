# Sing or hum a range of pitches and see the pitch detected in hz printed below.
# Press ctrl-c in the terminal when you're done to see a chart of the recorded pitches

# structure based on aubio demo, just replacing aubio package with fft
# https://github.com/aubio/aubio/blob/master/python/demos/demo_pyaudio.py

import pyaudio
import wave
import numpy
import fft
import matplotlib.pyplot as plt
import copy


def record():
    # initialise pyaudio
    p = pyaudio.PyAudio()

    # open stream
    buffer_size = 1024
    pyaudio_format = pyaudio.paFloat32
    n_channels = 1
    samplerate = 44100
    stream = p.open(format=pyaudio_format,
                    channels=n_channels,
                    rate=samplerate,
                    input=True,
                    frames_per_buffer=buffer_size)

    print("Start recording")

    frames = []

    # setup pitch
    tolerance = 0.8
    win_s = 4096 # fft size/window size
    hop_s = buffer_size # hop size
    #overlap is 4 for now
    testing = []

    temp = []

    try:
        while True:
            data = stream.read(buffer_size)
            frames.append(data)
            #while len(data) == buffer_size*5:
            decoded = numpy.frombuffer(data, dtype='float32')
            mag = numpy.frombuffer(data, dtype='float32')
            temp.extend(decoded)
            if len(temp)>=win_s:
                transform = fft.doFft(temp)
                #print(sum(abs(mag))/len(mag))
                if sum(abs(mag))/len(mag)>=0:
                    freq = getFreq(transform,win_s,samplerate)
                    if freq!=None and int(freq) != 0:
                        #print(int(freq))
                        testing.append(int(freq))
                temp = []       
    except KeyboardInterrupt:
        print("Done recording")
    except Exception as e:
        print(str(e))
    
    rng = list(range(len(testing)))
    plt.scatter(rng, testing)
    plt.ylabel('frequency in hz')
    plt.xlabel('time')
    plt.show()
    # real = []
    # imaginary = []
    # time = list(range(len(decoded)))
    # for i in decoded:
    #     real.append(i.real)
    #     imaginary.append(i.imag)
    # plt.plot(time, real)
    # plt.ylabel('intensity')
    # plt.xlabel('time')
    # plt.show()

    # if len(sys.argv) > 1:
    #     # record 5 seconds
    #     output_filename = sys.argv[1]
    #     record_duration = 5 # exit 1
    #     #outputsink = aubio.sink(sys.argv[1], samplerate)
    #     total_frames = 0
    # else:
    #     # run forever
    #     outputsink = None
    #     record_duration = None




    #audiobuffer = stream.read(buffer_size,exception_on_overflow = False)

    stream.stop_stream()
    stream.close
    p.terminate()

def record_to_file(file_path):
	wf = wave.open(file_path, 'wb')
	wf.setnchannels(CHANNELS)
	sample_width, frames = record()
	wf.setsampwidth(sample_width)
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()

def getFreq(array,buffer_size,samplerate):
    def indexToFreq(val):
        index = array.index(val)
        return index/buffer_size*samplerate
    array = array[0:len(array)//2]
    temp = []
    for i in array:
        temp.append(abs(i))
    array = copy.copy(temp)
    maximums = []
    # list of harmonics
    frequencies = []
    seen = False
    tempMax = max(temp)
    while tempMax>10:
        tempFreq = indexToFreq(tempMax)
        seen = False
        tempMax = max(temp)
        temp.remove(tempMax)
        for i in frequencies:
            if almostEqual(i,tempFreq,200):
                seen = True
                break
        if not seen and tempFreq >= 150:
            maximums.append(tempMax)
            
            frequencies.append(tempFreq)

    if frequencies != []:
        print(sorted(frequencies))
        return min(frequencies)


def almostEqual(a,b,round):
    if abs(a-b)<=round:
        return True
    return False
record()