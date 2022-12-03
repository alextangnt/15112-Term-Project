import cmath

# Cooley-Tukey FFT Algorithm
# https://en.wikipedia.org/wiki/Cooley%E2%80%93Tukey_FFT_algorithm
def doFft(vals):
    N = len(vals)
    if N == 1:
        return [vals[0]]
    else:
        Wn = cmath.exp(2j*cmath.pi/N)
        W = 1
        evenList = []
        oddList = []
        for i in range(N):
            if i%2 == 0:
                evenList.append(vals[i])
            else:
                oddList.append(vals[i])
        Y = [0]*N
        Yeven = doFft(evenList)
        Yodd = doFft(oddList)
        for i in range(N//2):
            Y[i] = Yeven[i]+W*Yodd[i]
            Y[(N//2)+i] = Yeven[i]-W*Yodd[i]
            W = W*Wn
        return Y


#print(calcWn([0,1,0,-1]))