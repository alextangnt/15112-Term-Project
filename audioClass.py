# Mark Newman series on decoding pitch information from an FFT
# Where is frequency? https://www.youtube.com/watch?v=3aOaUv3s8RY
# Where is magnitude and phase? https://www.youtube.com/watch?v=rUtz-471LkQ
# Why is output symmetrical? https://www.youtube.com/watch?v=IIofPiVVC64

# Negative Frequency by Iain Explains https://www.youtube.com/watch?v=gz6AKW-R69s

import fft
import pyaudio
import numpy as np
import copy

class Recording():
    noiseMag = 0.003
    minPitch = 100
    maxPitch = 500
    def __init__(self, outputHeight = 500):
        self.outputHeight = outputHeight
        # initialise pyaudio
        self.p = pyaudio.PyAudio()

        # open stream
        self.buffer_size = 1024
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