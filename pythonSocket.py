from socketIO_client import SocketIO, LoggingNamespace

class socketController:
    def __init__(self,address,port):
        self.socket=SocketIO(address,port,LoggingNamespace)
        self.socket.on('connect',self.onConnect)
        self.socket.on('disconnect',self.onDisconnect)

    def onConnect(self):
        print("connected to socket")
    def onDisconnect(self):
        print("Disconnected to socket")

    def sendData(self,event,data):
        self.socket.emit(event,data)




if __name__ == '__main__':
     s=socketController('localhost',8080)
     s.sendData('emg','open')
