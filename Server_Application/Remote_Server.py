import socket
import time
from lib.OrderManager import OrderManager


def sendMsg(connection, msg):
    try:
        msgOut = msg.encode(encoding='UTF-8',errors='replace')
        connection.send(msgOut)
        return True
    except:
        return False


def readMsg(connection):
    rec = ""
    info = {'plcActive': False,'conveyor': False, 'isStopperDown': True, 'orderComp': False, 'lastCarrierID': 0}
    try:
        rec = str(connection.recv(1024).decode('UTF-8'))
        #rec = "1:0:0:1:19"
        
        info['plcActive'] = bool(int(rec.split(':')[0]))
        info['conveyor'] = bool(int(rec.split(':')[1]))
        info['isStopperDown'] = bool(int(rec.split(':')[2]))
        info['orderComp'] = bool(int(rec.split(':')[3]))
        info['lastCarrierID'] = int(rec.split(':')[4])
    except:
        #print('ERROR: readMsg() exception hit')
        info['plcActive'] = False
        info['conveyor'] = True
        info['isStopperDown'] = False
        info['orderComp'] = False
        info['lastCarrierID'] = 0
        pass

    return info


def connect(HOST_IP, PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates the socket object 
    s.bind((HOST_IP, PORT)) # Associates the socket with a specific ip and port
    s.listen(1) # Number of unaccepted connections that the system will allow   
    c, addr = s.accept() # Blocks and waits for an incoming connection
    return c 


def main():
    HOST_IP = '127.0.0.1' #'172.20.40.44' # This is the Server's ethernet ip address
    PORT = 1234  # This is the port that will be used (non-privileged ports are > 1023)

    print("The IP address is: " + HOST_IP)

    o = OrderManager()

    print('Waiting for a connection')
    order = [0, 0, 0, 0, 0]
    mainRun = True
    newOrder = True
    while mainRun:
        msg = ""
        rec = {}

        tcpRun = True
        while tcpRun: 
            c = connect(HOST_IP, PORT)
            enMsg = "0:0:0:0:0"
            sendMsg(c, enMsg)
            rec = readMsg(c)
            if rec['plcActive']:
                tcpRun = False

        if newOrder:
            for x in range(0, len(order)):
                order[x] = 0
            o.startMenu()
            order = o.itemSelection()
            msg = o.formatOrder(order)
            newOrder = False 

        orderRun = True
        while orderRun:
            c = connect(HOST_IP, PORT)
            sendMsg(c, msg)
            rec = {}
            rec = readMsg(c)
            if rec['orderComp']:
                newTemp = ""
                newTemp = input('\n     Do you want to place another order?(y/n) ')
                if newTemp == 'y':
                    newOrder = True
                else:
                    mainRun = False
                orderRun = False

    print('\n   Thank you for ordering at SS import ;)')
    c.close()

main()

