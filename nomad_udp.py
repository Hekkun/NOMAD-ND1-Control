import sys
import socket
import codecs
import threading
from pynput import keyboard
from time import sleep, time

# Constants & Globals
NOMADIP = '192.168.0.1' # Since WiFi connection gateway is NOMAD, the IP is fixed
NOMAD_IPID = NOMADIP.split('.')[2] # Use to identify which host IP is on the NOMAD network
PORT = 8234 # Port is same for both host and NOMAD

MSG_CONNECT_STR = b'MAKO_CONNECT'
MSG_DISCONNECT_STR = b'MAKO_DISCONNECT'
MSG_READBATT_STR = b'MAKO_READ_BATT'
MSG_HEADER_STR = 'c0a8010100000421'
MSG_NO_OP = codecs.decode('c0a8010100000421000080', 'hex')

MSG_NM_CONNECT_OK_STR = b'CONNECT_OK\n'
MSG_NM_REJECT_STR = b'MAKO_REJECT\n'

keys_currently_pressed = {}

def sendmsg(sock, ip, PORT, msg, repeat=1, initialsleep = 0, finalsleep = 0):
    sleep(initialsleep)
    for i in range(0, repeat):
        sock.sendto(msg, ((ip, PORT)))
        sleep(finalsleep)

def recvmsg(sock, ip, PORT, buffsize=1024, num_msgs=1, initialsleep = 0, finalsleep = 0):
    sleep(initialsleep)
    msg = []
    for i in range(0, num_msgs):
        data, addr = sock.recvfrom(buffsize)
        print("Received message from: " + str(addr[0]) + ":" + str(addr[1]))
        print("Received message: %s" % data)
        msg.append(data)
    
    sleep(finalsleep)
    return msg

#######################################################
# dir range 
#   FWD = 1 to 255
#   REV = -255 to -1
# turn range
#   RIGHT = 1 to 127
#   LEFT = -127 to -1
#######################################################
def move(dir=0, turn=0, movehex='', turnhex=''):
    if (dir >= 0):
        movestr = format(dir, '02x') + '00'
    else:
        movestr = '00' + format(dir * -1, '02x')
    
    turnstr = format(turn + 128, '02x')

    if movehex:
        movestr = movehex
    
    if turnhex:
        turnstr = turnhex

    return codecs.decode(MSG_HEADER_STR + movestr + turnstr, 'hex')

def setupconn():
    hostname, aliaslist, ipaddrlist = socket.gethostbyname_ex(socket.gethostname())
    srcip = ''
    for ip in ipaddrlist:
        if(ip.split('.')[2] == NOMAD_IPID):
            # This is the IP address of the current device on the NOMAD network
            srcip = ip

    if(not srcip): 
        print("Not connected to NOMAD WiFi network!")
        exit(11)
    else:
        print("Connected to NOMAD WiFi! \nNOMAD IP = " + NOMADIP + "\nHost IP = " + srcip)

    rxsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Open a UDP socket
    rxsocket.bind((srcip, PORT))
    rxsocket.settimeout(10)

    sendmsg(rxsocket, NOMADIP, PORT, MSG_DISCONNECT_STR)
    msg = recvmsg(rxsocket, NOMADIP, PORT, finalsleep=1)

    sendmsg(rxsocket, NOMADIP, PORT, MSG_CONNECT_STR)
    msg = recvmsg(rxsocket, NOMADIP, PORT, finalsleep=1)
    if (msg[0] != MSG_NM_CONNECT_OK_STR):
        print("Connection failure! Unexpected response: %s" % msg[0])
        exit(10)

    sendmsg(rxsocket, NOMADIP, PORT, MSG_READBATT_STR)
    msg = recvmsg(rxsocket, NOMADIP, PORT, finalsleep=0.2)

    sendmsg(rxsocket, NOMADIP, PORT, MSG_NO_OP)
    msg = recvmsg(rxsocket, NOMADIP, PORT, finalsleep=1)

    return rxsocket

def movetest(rxsocket):
    sendmsg(rxsocket, NOMADIP, PORT, move(movehex='0000', turnhex='81'), finalsleep=0.1, repeat=5)
    sendmsg(rxsocket, NOMADIP, PORT, move(movehex='0000', turnhex='d2'), finalsleep=0.1, repeat=5)
    sendmsg(rxsocket, NOMADIP, PORT, move(movehex='4400', turnhex='d2'), finalsleep=0.1, repeat=5)
    sendmsg(rxsocket, NOMADIP, PORT, move(movehex='4400', turnhex='80'), finalsleep=0.1, repeat=5)
    sendmsg(rxsocket, NOMADIP, PORT, move(movehex='0044', turnhex='7f'), finalsleep=0.1, repeat=5)
    sendmsg(rxsocket, NOMADIP, PORT, move(movehex='0044', turnhex='2e'), finalsleep=0.1, repeat=5)
    sendmsg(rxsocket, NOMADIP, PORT, move(movehex='0000', turnhex='81'), finalsleep=0.1, repeat=5)
    sendmsg(rxsocket, NOMADIP, PORT, move(movehex='0000', turnhex='d2'), finalsleep=0.1, repeat=5)
    sendmsg(rxsocket, NOMADIP, PORT, move(movehex='4400', turnhex='d2'), finalsleep=0.1, repeat=5)
    sendmsg(rxsocket, NOMADIP, PORT, move(movehex='4400', turnhex='80'), finalsleep=0.1, repeat=5)
    sendmsg(rxsocket, NOMADIP, PORT, move(movehex='0044', turnhex='7f'), finalsleep=0.1, repeat=5)
    sendmsg(rxsocket, NOMADIP, PORT, move(movehex='0044', turnhex='2e'), finalsleep=0.1, repeat=5)
    sendmsg(rxsocket, NOMADIP, PORT, move(movehex='0000', turnhex='81'), finalsleep=0.1, repeat=5)
    sendmsg(rxsocket, NOMADIP, PORT, move(movehex='0000', turnhex='d2'), finalsleep=0.1, repeat=5)
    sendmsg(rxsocket, NOMADIP, PORT, MSG_NO_OP, finalsleep=2)
    sendmsg(rxsocket, NOMADIP, PORT, move(movehex='4400', turnhex='d2'), finalsleep=0.1, repeat=5)
    sendmsg(rxsocket, NOMADIP, PORT, move(movehex='4400', turnhex='80'), finalsleep=0.1, repeat=5)
    sendmsg(rxsocket, NOMADIP, PORT, move(movehex='0044', turnhex='7f'), finalsleep=0.1, repeat=5)
    sendmsg(rxsocket, NOMADIP, PORT, move(movehex='0044', turnhex='2e'), finalsleep=0.1, repeat=5)
    sendmsg(rxsocket, NOMADIP, PORT, MSG_NO_OP, finalsleep=2)

    sendmsg(rxsocket, NOMADIP, PORT, MSG_READBATT_STR)
    msg = recvmsg(rxsocket, NOMADIP, PORT, finalsleep=0.2)

    sendmsg(rxsocket, NOMADIP, PORT, MSG_NO_OP, finalsleep=2)

def turntest(rxsocket):
    for i in range (-127, 0):
        sendmsg(rxsocket, NOMADIP, PORT, move(0, i), repeat=1, finalsleep=0.1)
        print(i)
    
    sleep(5)

    for i in range (0, 128):
        sendmsg(rxsocket, NOMADIP, PORT, move(0, i), repeat=1, finalsleep=0.1)
        print(i)

def disconnect(rxsocket):
    sendmsg(rxsocket, NOMADIP, PORT, MSG_NO_OP, repeat=2, finalsleep=0.1)
    sendmsg(rxsocket, NOMADIP, PORT, MSG_DISCONNECT_STR)
    msg = recvmsg(rxsocket, NOMADIP, PORT)

def on_press(key):
    global keys_currently_pressed # global is needed to enable modification, not needed for read

    if key not in keys_currently_pressed:
        keys_currently_pressed[key] = time()

def on_release(key):
    global keys_currently_pressed

    if key in keys_currently_pressed:
        duration = time() - keys_currently_pressed[key]
        print("The key", key, "was pressed for", str(duration)[0:5], "seconds")
        del keys_currently_pressed[key]

    if key == keyboard.Key.esc:
        # Stop listener
        return False
    
def startkbcontrol(rxsocket):
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        print("Press the [Esc] key to stop NOMAD control and exit.")
        constspeed = 55
        boostspeed = 70
        boost_enable = 0

        constturn = 40
        boostturn = 50
        turnboost_enable = 0

        while listener.is_alive():
            sleep(0.1)
            dir = 0
            turn = 0
            # print(keys_currently_pressed) 
            if keyboard.Key.shift in keys_currently_pressed:
                boost_enable = 1
            else:
                boost_enable = 0

            if keyboard.Key.space in keys_currently_pressed:
                turnboost_enable = 1
            else:
                turnboost_enable = 0
            
            if keyboard.Key.up in keys_currently_pressed and keyboard.Key.down in keys_currently_pressed:
                print("Ignoring overlapped input up & down")
            else:
                if keyboard.Key.up in keys_currently_pressed:
                    dir = constspeed + boost_enable * boostspeed
                if keyboard.Key.down in keys_currently_pressed:
                    dir = -(constspeed + boost_enable * boostspeed)
            
            if keyboard.Key.left in keys_currently_pressed and keyboard.Key.right in keys_currently_pressed:
                print("Ignoring overlapped input left & right")
            else:
                if keyboard.Key.left in keys_currently_pressed:
                    turn = -(constturn + turnboost_enable * boostturn)
                if keyboard.Key.right in keys_currently_pressed:
                    turn = constturn + turnboost_enable * boostturn
            
            sendmsg(rxsocket, NOMADIP, PORT, move(dir, turn))
            # print(dir, turn)

        listener.join()

def main(args):
    rxsocket = setupconn()
    
    # movetest(rxsocket)
    # turntest(rxsocket)

    startkbcontrol(rxsocket)

    disconnect(rxsocket)

if (__name__ == "__main__"):
    main(sys.argv)