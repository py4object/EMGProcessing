from numpy import sin, linspace, pi,loadtxt,fix,delete,savetxt
from pylab import plot, show, title, xlabel, ylabel, subplot,figure
from scipy import fft, arange
import sys


def fq(y):
    Fs = 1000;  # sampling rate
    Fn=Fs/2
    L=len(y)
    Ts=arange(0,L)/float(Fs)
    Femg=fft(y)*2/L
    FreqVector=linspace(0,1,fix(L/2))*Fn
    indexV=arange(1,len(FreqVector))
    subplot(2,1,1)
    xlabel('Time')
    ylabel('Amplitude')
    # subplot(2,1,2)
    Femg=abs(Femg[indexV])
    # print (len(Femg))
    FreqVector=delete(FreqVector,len(FreqVector)-1)

    return FreqVector,Femg




inputs=(sys.argv[2:len(sys.argv)])
rawFiles=[]
for input in inputs:
    rawFiles.append(loadtxt(fname=input))
print len(rawFiles)
attr,x=fq(rawFiles[1])
values=[]
for rawFile in rawFiles:
    a,value=fq(rawFile)
    values.append(value)
print(len(values))
# print(values[0])

result="@RELATION adsa\n"
for att in attr:
    result+="@ATTRIBUTE {0} numeric\n".format(att)

result+="@DATA\n"
for value in values:
    result+=( ",".join(format(x, "10.3f") for x in value))
    result+=("\n")
text_file = open("Output.txt", "w")
text_file.write(result)
text_file.close()
