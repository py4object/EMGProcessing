class test:
    def __init__(self):
        self.x=list()
    def bo(self):
        for i in range(100):
            for d in self.x:
                d(i)
    def mname(self,n):
        print n
    def addCallBack(self,fn):
        self.x.append(fn)


def nn(i):
    print ('bo')
if __name__ == '__main__':
    t=test()
    t.addCallBack(t.mname)
    t.addCallBack(nn)
    t.bo()
