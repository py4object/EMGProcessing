
  # -*- coding: utf-8 -*-

import serial,thread,time
import sys
import matplotlib.pyplot as plt
from collections import deque
import matplotlib.animation as animation
import thread
import numpy as np
from numpy import *
import scipy
from scipy import *
from Tkinter import *
import Tkinter as tk
import time,datetime
from nn import init,classfiy1,classfiy2
import requests
import json
from pythonSocket import socketController


class DataRecorder:
    def __init__(self,tty,serialSpeed,outputPath,upthreshold=5,downthreshold=5,isThresholdRelativeToMean=True,preLength=10,postLength=120,mode='threshold'):
        self.ser=serial.Serial(tty,serialSpeed)
        self.isThresholdRelativeToMean=isThresholdRelativeToMean
        self.upthreshold=upthreshold
        self.outputPath=outputPath
        self.downthreshold=downthreshold
        self.__isReading=False
        self.__inputLisners=[]
        self.maxPlotLen=500
        self.plotY=deque([0.0]*self.maxPlotLen)
        self.plotX=np.arange(0,self.maxPlotLen)
        self.figure=plt.figure()
        self.minY=200
        self.maxY=300
        self.plt= plt.axes(xlim=(0, self.maxPlotLen), ylim=(self.minY,self.maxY))
        self.plt.grid(True)
        self.line,=self.plt.plot([],[],lw=2)
        self.mean=-1
        self.buffer=deque()
        self.inCapturing=False
        self.pre=preLength
        self.post=postLength
        self.__caputredSignalListner=[]
        self.fff=0;
        self.socketController=socketController('localhost',8080)
        init()



    def startReading(self):
        if self.__isReading==True:
            return
        self.__isReading=True
        thread.start_new_thread(self.__startReading,())

    def __readIntFromSerial(self):
        while True:
            try:
                value=self.ser.readline().strip()
                if type(value) !=int:
                    value=int(value)
                if value>100:
                    return value
            except   Exception as e:
                print(str(e))


    def __startReading(self):
        self.ser.reset_input_buffer()
        while self.__isReading:
                if self.isThresholdRelativeToMean==True and self.mean ==-1:
                    tempArray=[]
                    print('plz hold static while calculating the mean')
                    for i in range(1000):
                        print_progress(iteration=i,total=999)
                        tempArray.append(self.__readIntFromSerial())
                    self.mean=sum(tempArray)/float(len(tempArray))
                    print ("the mean is "+str(self.mean))
                    self.upthreshold=self.mean+self.upthreshold
                    plt.axhline(y=self.upthreshold)
                    self.downthreshold=self.mean-self.downthreshold
                    plt.axhline(y=self.downthreshold)
                    self.plt.relim()
                    # plt.autoscale()
                    # self.plt.autoscale_view()
                    # self.plt.hide()
                    plt.draw()
                    print(str(self.upthreshold) +" "+str(self.downthreshold))
                value=self.__readIntFromSerial()
                for callback in self.__inputLisners:
                    callback(value)


    def stopRecording(self):
        self.__isReading=False

    def addCallBack(self, fn):
        self.__inputLisners.append(fn)

    def updatePlot(self, i):
        self.line.set_data(self.plotX,self.plotY)
        try:
            self.plt.set_ylim([min(self.plotY)-5,max(self.plotY)+5])

            pass
        except Exception as e:
            raise
        else:
            pass

        return self.line,

    def showPlot(self):
        self.addCallBack(self.__updatePlotData)
        aim=animation.FuncAnimation(self.figure,self.updatePlot,  frames=200, interval=20, blit=True)
        plt.show()


    def __updatePlotData(self, i):
        self.plotY.popleft()
        self.plotY.append(i)
        if self.minY!=min(self.plotY) or self.maxY!=self.minY:

            self.plt.relim()
            # self.plt.autoscale_view()
            plt.draw()

    def thresholdCapture(self, i):
        self.buffer.append(i)
        if (i >self.upthreshold or i <self.downthreshold) and not self.inCapturing :
            self.inCapturing=True
            # print('in capturing')
        if(self.pre+self.post ==len(self.buffer)) and self.inCapturing==True:
            self.inCapturing=False
            fftEmg=self.fft(self.buffer)
            buffer=self.buffer
            self.buffer=deque()
            for callback in self.__caputredSignalListner:
                callback(buffer,fftEmg)

        elif not self.inCapturing:
            if(len(self.buffer)==self.pre):
                self.buffer.popleft()

# def thresholdCapturev2(self,i):
#     self.buffer.append(i)
#     if (i >self.upthreshold or i <self.downthreshold) and not self.inCapturing :
#             self.inCapturing=True



    def fft(self,y):
        Fs = 1000;  # sampling rate
        Fn=Fs/2
        L=len(y)
        Ts=arange(0,L)/float(Fs)
        Femg=scipy.fft(y)*2/L
        FreqVector=linspace(0,1,fix(L/2))*Fn
        indexV=arange(1,len(FreqVector))
        Femg=abs(Femg[indexV])
        return Femg


    def handleCapturedSignal(self, record,ffemg):
        self.rawRecord=record
        self.ffemgRecord=ffemg
        self.stopRecording()
        self.showSaveMsg()

    def registerFemgHandler(self, fn):
        self.__caputredSignalListner.append(fn)

    def examnLiveData(self,raw,ffemg):
        pass
        print("we are trying to classfiy it !!!!!" +str(self.fff))
        self.fff=self.fff+1
        result= (classfiy1([ffemg]))
        print result
        self.socketController.sendData('emg',result)
        print (classfiy2([ffemg]))
        print("--------------------------------------")

    def handleCapturedSignalW(self, record,ffemg):
        self.rawRecord=record
        self.ffemgRecord=ffemg
        self.stopRecording()
        result= (classfiy1([ffemg]))

        self.showSaveMsg(msg=result)





    def showSaveMsg(self,msg=''):
        root=Tk()
        self.root=Frame(root)
        lable=Label(self.root,text="please enter the the MovmentType")
        v = StringVar()
        filename=Entry(self.root,textvariable=v)
        lable.pack()
        filename.pack()
        filename.insert(0,msg)
        self.saveSubjectName=filename
        saveButton=Button(self.root,text="save",command=self.save)
        cancleButton=Button(self.root,text="cancle",command=self.cleanup)
        saveButton.pack()
        cancleButton.pack()
        self.xx=root
        self.root.pack()
        root.mainloop()


    def save(self):
        print ('saved')
        inFileName=self.saveSubjectName.get()
        ts=time.time()
        print(self.ffemgRecord)
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')
        np.savetxt(fname=self.outputPath+st+"_"+inFileName.upper()+".raw",fmt='%i',X=self.rawRecord)
        np.savetxt(fname=self.outputPath+st+"_"+inFileName.upper()+".fq",X=self.ffemgRecord)
        self.cleanup()


    def cleanup(self):
        self.root.destroy()
        self.startReading()
        self.xx.withdraw()




def post(result):
    # requests.post('http://10.151.42.251:8000/api/pizza/da',json={"data":result.lower()})
    pass
def print_progress(iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    """
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()
def pr(i):
    # print (i)

    pass

if __name__ == '__main__':
    try:
        pass

        recorder=DataRecorder(tty='/dev/ttyACM0',serialSpeed=115200,outputPath="data_repo/raw/6_6_1_120/Omar/",isThresholdRelativeToMean=True,upthreshold=6,downthreshold=6,postLength=120,preLength=1)
        recorder.addCallBack(pr)
        recorder.registerFemgHandler(recorder.examnLiveData)
        recorder.addCallBack(recorder.thresholdCapture)
        recorder.startReading()
        recorder.showPlot()
    # recorder.showSaveMsg()
    except Exception as e:
        raise
    else:
        pass
