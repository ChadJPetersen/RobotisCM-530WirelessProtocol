#Chad J Petersen
#3/28/2015
#UWYO ACM

import time, sys, serial

# SERIAL INIT
defaultPort = "COM5" # change to suit your needs
ser = serial.Serial()
TIMEOUT = 5 # max number of sensor request attempts

#servo ID's 
BROADCASTID = 254


def initCom(port):
    ser.baudrate = 38400
    ser.port = port
    ser.timeout = 0.5
    ser.open()

def closeCom():
    ser.close() # close serial connection so it is available in future
# end SERIAL INIT

# PACKET HANDLING
def readPacket():
    frameIncomplete = True
    frameByteIndex = -1
    checkSum = 0
    packet = [0, 0, 0, 0, 0, 0]
    #print('reading packet...')
    while ser.inWaiting() > 0 and frameIncomplete:
        byteValue = repr(ser.read()).lstrip('b').strip('\'')
    #print repr(byteValue)
        if len(byteValue) != 4: # python uses Unicode in some cases instead of hex
            if byteValue == '\\\\': # python hex value is converted to char
                value = 92 # correct value
            elif byteValue == '\\t':
                value = 9
            elif byteValue == '\\n':
                value = 10
            else:
                value = ord(byteValue)
        else:
            value = int(byteValue.lstrip('\\').lstrip('x'), 16)
        #print('read: ' + byteValue + '...')
        if frameByteIndex == -1:
            if value == 255: # encountered frame beginning
                frameByteIndex = 0
                #print('frame start...')
        elif frameByteIndex == 6: # frame is complete
            packetCheckSum = ser.read()
            frameIncomplete = False
            # TODO: verify checkSum here
        else: # get values in frame
            packet[frameByteIndex] = value
            checkSum = checkSum + value
            frameByteIndex = frameByteIndex + 1
    #print('packet complete...')
    return packet

def sendPacket(packet):
    # packet format is list of 6 8-bit chars/values
    # information on packet transmition can be fount at
    # http://support.robotis.com/en/product/dynamixel/communication/dxl_packet.htm
    # with more information on exact methods at
    # http://support.robotis.com/en/product/dynamixel/ax_series/dxl_ax_actuator.htm
    # (0xFF 0xFF) This signal notifies the beginning of the packet
    ser.write('\xFF') # begin frame
    ser.write('\xFF')
    ser.write(chr(packet[0] + 128)) #Servo ID
    ser.write(chr(packet[1] + 128)) #It is the length of the packet. The length is calculated as “the number of Parameters (N) + 2”
    ser.write(chr(packet[2] + 128)) #This command gives an instruction to Dynamixel 
    ser.write(chr(packet[3] + 128)) #Parameter is used when Instruction requires ancillary data.
    ser.write(chr(packet[4]))
    ser.write(chr(packet[5]))
    ser.write(chr(255 - ((packet[0] + packet[1] + packet[2] + packet[3] + packet[4] + packet[5]) % 256))) # checksum
    # Check Sum = ~ ( ID + Length + Instruction + Parameter1 + … Parameter N )
    # Where, “~” is the Not Bit operator.
    time.sleep(0.030303030303030303) # this very roughly sends commands at 33Hz
# end PACKET HANDLING