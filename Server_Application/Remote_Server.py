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

def Msg(convOn, orderMsg):
    msg = str(int(convOn))
    msg += ':'
    msg += orderMsg
    return msg

def readMsg(connection):
    rec = ""
    info = {'plcActive': False,'conveyor': False, 'isStopperDown': True, 'orderNotComp': True, 'lastCarrierID': '0'}
    try:
        rec = str(connection.recv(10).decode('UTF-8'))
        #rec = "1:0:0:1:19"

        info['plcActive'] = bool(int(rec.split(':')[0]))
        info['conveyor'] = bool(int(rec.split(':')[1]))
        info['isStopperDown'] = bool(int(rec.split(':')[2]))
        info['orderNotComp'] = bool(int(rec.split(':')[3]))
        info['lastCarrierID'] = str(rec.split(':')[4])
    except:
        info['plcActive'] = True
        info['conveyor'] = True
        info['isStopperDown'] = False
        info['orderNotComp'] = False
        info['lastCarrierID'] = 0

    return info


def main():
    HOST_IP = '192.168.87.103' #'172.20.40.44' # This is the Server's ethernet ip address
    PORT = 55234  # This is the port that will be used (non-privileged ports are > 1023)

    print("The IP address is: " + HOST_IP)

    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates the socket object 
    #s.bind((HOST_IP, PORT)) # Associates the socket with a specific ip and port

    o = OrderManager()

    print('Waiting for a connection')
    order = [0, 0, 0, 0, 0]
    mainRun = True
    newOrder = True
    while mainRun:      # Ordering loop
        msg = ""
        rec = {}

        tcpRun = True
        while tcpRun: 
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates the socket object 
            s.bind((HOST_IP, PORT)) # Associates the socket with a specific ip and port

            s.listen(5) # Number of unaccepted connections that the system will allow   
            c, addr = s.accept() # Blocks and waits for an incoming connection
            enMsg = "0:0:0:0:0"
            sendMsg(c, enMsg)
            rec = readMsg(c)
            print(str(rec))
            if rec['plcActive']:
                tcpRun = False
            

        if newOrder:
            for x in range(0, len(order)):
                order[x] = 0
            o.startMenu()
            order = o.itemSelection()
            msg = o.formatOrder(order)
            print('msg: ' + str(msg))
            newOrder = False 

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates the socket object 
        s.bind((HOST_IP, PORT)) # Associates the socket with a specific ip and port

        s.listen(5) # Number of unaccepted connections that the system will allow   
        c, addr = s.accept() # Blocks and waits for an incoming connection 

        print('Connected to client')
        cRun = True
        try:
            if sendMsg(c, msg):
                readRun = True
                while readRun:      # Read loop
                    rec = readMsg(c)
                    print('rec: ' + str(rec))
                    try:
                        readRun = rec['orderNotComp'] 
                    except:
                        pass
                c.close()
                newTemp = ""
                newTemp = input('\n     Do you want to place another order?(y/n) ')
                if newTemp == 'y':
                    newOrder = True
                else:
                    mainRun = False
            else:
                cRun = False
        except:
            pass

    print('\n   Thank you for ordering at SS import ;)')
            

main()




def mainOLD():
    host_ip = '192.168.87.103' #'172.20.40.44' # This is the Server's ethernet ip address
    port = 2234  # This is the port that will be used (non-privileged ports are > 1023)

    print("The IP address is: " + host_ip)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates the socket object 
    s.bind((host_ip, port)) # Associates the socket with a specific ip and port
    

    o = OrderManager() 

    inc = 0
    msg = ""
    print('Waiting for a connection')
    while True:

        #c, addr = s.accept() # Blocks and waits for an incoming connection 
        #print('Connecting...')
        try:
            #inc = int(c.recv(100).decode('UTF-8'))
            #o.startMenu()
            #msg = o.formatOrder(o.itemSelection())
            s.listen(5) # Number of unaccepted connections that the system will allow 
            c, addr = s.accept() # Blocks and waits for an incoming connection 
            #print('msg: ' + msg)
            sendMsg(c, '1:2:3:4:' + str(inc))
            print('1:2:3:4:' + str(inc))
            time.sleep(3)
            sendMsg(c, 'here')
            inc = inc +2
            c.close()### Caution!!
            #break
        except:
            pass


#mainOLD()
