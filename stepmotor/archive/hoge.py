import socket
import select
import time
import logging
import string
class controller(object):
    def __init__(self,ipaddr):
        self.ipaddr=ipaddr
        self.reply_message=None
        print "init controller"
        self.connect()
        
    def connect(self):
        netAddr=(self.ipaddr, 4001)
        self.netsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.netsock.connect(netAddr)
        self.netsock.setblocking(1)
        print "connect %s" % self.ipaddr 
        
    def __enter__(self):
        try:
            self.connect()
        except:
            print "error"
        print "enter"
        return self
                
    def read(self):
        #self.reply_message = self.netsock.recv(2048)[6:-2]
        data = self.netsock.recv(2048)[:-2]
        try:
            self.reply_message = int(data)
        except:
            self.reply_message = 0.881
            print "hoge"
        print "#",self.reply_message
        
    def send(self, sendString):
        print sendString
        self.netsock.send(sendString+'\n')

    def __exit__(self,type, value, traceback):
        self.netsock.close()
        print "exit controller"


if __name__=='__main__':
    c = controller('10.68.10.250')
    
