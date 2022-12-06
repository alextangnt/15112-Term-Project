# Try switching out 440.wav at the bottom with other file names in sample audios
# to see a frequency chart at one point + its waveform

# https://stackoverflow.com/questions/6951046/how-to-play-an-audiofile-with-pyaudio
import pyaudio
import wave
import numpy
import fft
import matplotlib.pyplot as plt
import math

class AudioFile:
    chunk = 1024

    def __init__(self, file):
        """ Init audio stream """ 
        self.wf = wave.open(file, 'rb')
        #get framerate in khz
        self.frameRate = self.wf.getframerate()/1000
        #print(self.wf.getframerate())
        self.p = pyaudio.PyAudio()
        print('stream starting')
        self.stream = self.p.open(
            format = self.p.get_format_from_width(self.wf.getsampwidth()),
            channels = self.wf.getnchannels(),
            rate = self.wf.getframerate(),
            output = True
        )

    def play(self):
        """ Play entire file """
        data = self.wf.readframes(self.chunk)
        allData = []
        #while data != b'':
        for i in range(100):
            self.stream.write(data)
            data = self.wf.readframes(self.chunk)
            
            self.decoded = numpy.frombuffer(data, dtype='int16',)
            allData.append(self.decoded)

        # for i in allData[0]:
        #     i = complex(i)
        #     print(i)
        #print(allData[0])
        
        transform = fft.doFft(allData[0])
        
        # print(transform)
        self.graph(transform)

        # avPitch = 0
        # for i in allData:
        #     avPitch += self.getFreq(fft.calcWn(i),self.chunk,self.frameRate)
        # print(avPitch/len(allData))

        rng = list(range(len(allData[0])))
        plt.plot(rng, allData[0])
        plt.ylabel('y')
        plt.xlabel('x')
        plt.show()

    def getFreq(self,array,buffer_size,samplerate):
        array = array[0:len(array)//2]
        maximum = max(array)
        maximum = abs(maximum)
        # freq = []
        for i in range(len(array)):
            p = abs(array[i])
            if p>=maximum:
                return (i/buffer_size*samplerate)
        # if freq!=[]:
        #     return(sum(freq)/len(freq))

    
    def graph(self,array):
        maximum = numpy.max(array)
        maximum = abs(maximum)
        pythag = []
        new = []
        thing = []

        
        index = 0
        array = array[0:len(array)//2]
        for i in array:
            new.append(math.atan2(i.imag,i.real))
            p = abs(i)
            if p>maximum-maximum//10:
            #     #print(p)
                 print(index/self.chunk*self.frameRate)
            pythag.append(abs(i))
            thing.append(i.real)
            index+=1


        rng = list(range(len(array)))
        newrng = []
        for i in rng:
            newrng.append(i/self.chunk*self.frameRate)
        plt.scatter(newrng[0:len(array)//2], pythag[0:len(array)//2])
        plt.ylabel('y')
        plt.xlabel('x')
        plt.show()

    def close(self):
        """ Graceful shutdown """ 
        self.stream.close()
        self.p.terminate()

a = AudioFile("audio tests/sample audios/voiceSample.wav")
a.play()
a.close()