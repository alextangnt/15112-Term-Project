# Mark Newman series on decoding pitch information from an FFT
# Where is frequency? https://www.youtube.com/watch?v=3aOaUv3s8RY
# Where is magnitude and phase? https://www.youtube.com/watch?v=rUtz-471LkQ
# Why is output symmetrical? https://www.youtube.com/watch?v=IIofPiVVC64

# Negative Frequency by Iain Explains https://www.youtube.com/watch?v=gz6AKW-R69s

import fft
import pyaudio
# using wave to read wav files
import wave
import numpy as np
import copy
import math

class Recording():
    noiseMag = 0.003
    minPitch = 100
    maxPitch = 500
    startingFreq = 196.00
    def __init__(self, outputHeight = 500,file=None):
        self.outputHeight = outputHeight
        
        # initialise pyaudio
        self.p = pyaudio.PyAudio()
        self.buffer_size = 1024

        # open stream
        pyaudio_format = pyaudio.paFloat32
        n_channels = 1
        self.samplerate = 44000
        self.stream = self.p.open(format=pyaudio_format,
                        channels=n_channels,
                        rate=self.samplerate,
                        input=True,
                        frames_per_buffer=self.buffer_size)

        self.frames = 0
        self.temp = []

        self.mag = 0
        self.pitchList = [outputHeight/2]
        self.magList = []
    
    def readFile(self):
        data = self.wf.readframes(self.buffer_size)
        while len(data):
            #self.stream.write(data)
            self.frames+=1
            decoded = np.frombuffer(data, dtype='int'+str(self.format))
            magList = np.frombuffer(data, dtype='int'+str(self.format))
            self.mag = sum(abs(magList))/len(magList)
            self.temp.extend(decoded)
            data = self.wf.readframes(self.buffer_size)

    def interpretFile(self):
        size = len(self.temp)
        n = self.buffer_size
        for i in range(0, size, n):
            chunk = self.temp[i:i + n]
            freq = Recording.getFreq(chunk, n, 44000)
            if freq != None:
               self.pitchList.append(int(freq))

    @staticmethod
    def almostEqual(a,b,round):
        if abs(a-b)<=round:
            return True
        return False

    @staticmethod
    def getFreq(array, win_size, samplerate):
        def indexToFreq(val):
            index = array.index(val)
            return index/win_size*samplerate
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
                if Recording.almostEqual(i,tempFreq,200):
                    seen = True
                    break
            if not seen and tempFreq >= 150:
                maximums.append(tempMax)
                
                frequencies.append(tempFreq)

        if frequencies != []:
            # print(frequencies)
            return min(frequencies)

    def processAudio(self):
        data = self.stream.read(self.buffer_size,exception_on_overflow = False)
        self.frames+=1
        decoded = np.frombuffer(data, dtype='float32')
        magList = np.frombuffer(data, dtype='float32')
        self.mag = sum(abs(magList))/len(magList)
        self.temp.extend(decoded)

    def makeFft(self,window):
        transform = fft.doFft(self.temp)
        if self.mag>=self.noiseMag:
            freq = self.getFreq(transform,self.buffer_size*window,self.samplerate)
            if freq!=None and int(freq) != 0:
                #print(int(freq))

                self.pitchList.append(freq)
        self.temp = []
        self.frames = 0
    
    def getCastFreq(self):
        castedVal = (self.pitchList[-1]-self.minPitch)/(self.maxPitch-self.minPitch)*self.outputHeight
        if castedVal > self.outputHeight:
            castedVal = self.outputHeight
        return castedVal
        #print(int(freq),int(castedVal))

    def getNoteFreq(self):
        # castedVal = (self.pitchList[-1]-self.minPitch)/(self.maxPitch-self.minPitch)*self.outputHeight
        # if castedVal > self.outputHeight:
        #     castedVal = self.outputHeight
        g3 = 196.00
        a3 = 220.65
        b3 = 246.94
        c4 = 261.63
        d4 = 293.66
        e4 = 329.63
        f4 = 349.23
        g4 = 392.00
        gOctave = [0,2,4,5,7,9,10,12]
        # using the formula Freq = note x 2^N/12 from
        # http://techlib.com/reference/musical_note_frequencies.htm#:~:text=Starting%20at%20any%20note%20the,be%20positive%2C%20negative%20or%20zero.
        freq = self.pitchList[-1]
        note = Recording.startingFreq
        N = freq/note
        N = 12*math.log(N)/math.log(2)
        
        N = round(N)
        #print(N)
        #print('audioclass ' + str(self.outputHeight/9))
        if N in gOctave:
            place = gOctave.index(N)+1
            return place*(self.outputHeight/9)
        for i in range(len(gOctave)-1):
            if gOctave[i]<N<gOctave[i+1]:
                return (i+1)*(self.outputHeight/9)
        if N<gOctave[0]:
            return self.outputHeight/9
        elif N>gOctave[-1]:
            return 8*self.outputHeight/9

    @classmethod
    def updateNoise(self,noise):
        if noise >= Recording.noiseMag:
            Recording.noiseMag = noise
    
    @classmethod
    def updateMaxPitch(self,highest):
        Recording.maxPitch = highest

    @classmethod
    def updateMinPitch(self,lowest):
        Recording.minPitch = lowest
    
    def pause(self):
        self.stream.stop_stream()

    def start(self):
        self.stream.start_stream()
            
    def end(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

# recorder = Recording(file = 'songs/AUNTRODY.wav')
# recorder.readFile()
# recorder.interpretFile()

# print(len(recorder.pitchList))
