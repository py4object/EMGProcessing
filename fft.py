from numpy import sin, linspace, pi,loadtxt,fix,delete,savetxt
from pylab import plot, show, title, xlabel, ylabel, subplot,figure
from scipy import fft, arange
import sys


Fs = 1000;  # sampling rate
Fn=Fs/2
y=loadtxt(fname=str(sys.argv[1]))
L=len(y)
Ts=arange(0,L)/float(Fs)
# print(Ts)
# t = arange(0,L-1,Ts)/Fs # time vector
Femg=fft(y)*2/L
FreqVector=linspace(0,1,fix(L/2))*Fn
indexV=arange(1,len(FreqVector))


subplot(2,1,1)


# plot(Ts,y)
xlabel('Time')
ylabel('Amplitude')
# subplot(2,1,2)
Femg=abs(Femg[indexV])
# print (len(Femg))
FreqVector=delete(FreqVector,len(FreqVector)-1)
# print((FreqVector))

result=[i for i in FreqVector ]
# print (result)
result2=Femg[0:len(result)]
# print((result2))

# result=Femg[result]
fname=sys.argv[1]
fname=fname.replace("raw","fq")
# print(fname)
savetxt(fname=fname,X=result2)
# savetxt(fname=sys.argv[1]+"vect",X=FreqVector)

# plot(FreqVector,Femg)1121
# figure()
subplot(1,1,1)
plot(result,result2)
# show()#
