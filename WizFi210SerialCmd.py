import time
import serial
import socket
import struct


class WizFi210SerialCmd(object):

    def __init__(self, comP, baud, timeoutValue):
        self.ser = serial.Serial(comP, baud, timeout = timeoutValue)

    def serialClose(self):
        self.ser.close()
    
    def __del__(self):
        self.serialClose()

    def Write_CMD(self,cmd, resp1, resp2, ngtvResp, loopCnt, opt=1):
        status = False
        resp1_stat = False
        resp2_stat = False

        if( opt == 1 ):
            cmd = cmd + "\r"
        
        self.ser.write(cmd)

        for i in range(loopCnt):
            respData = self.ser.readline()
            if( respData != ""):
                print respData
            
            if( respData.find(resp1) >= 0 ):
                resp1_stat = True
            elif( respData.find(resp2) >= 0):
                resp2_stat = True
            elif( respData.find(ngtvResp) >= 0):
                return False
                
            if( resp1_stat == True and resp2_stat == True):
                status = True
                break
        
        return status
    
    def flush_serial(self):
        respData = self.ser.readline()
        if( respData != ""):
            print respData
        
        
COM_PORT = "/dev/ttyUSB0"
BAUDRATE = 115200
SSID     = "WiznetKaizen"
PASSWORD = "qazxswedc"

SRC_IP      = "192.168.201.21"
SRC_ADDR    = "\x00\x08\xDC\x00\x00\x00"
DEST_IP     = "192.168.201.6"
DEST_ADDR   = "\x50\xE5\x49\x00\x00\x00"
SRC_PORT    = 5000
DEST_PORT   = 5000


def make_ipv4_header(srcip, dstip, datal, srcprt, dstprt):
    srcip = socket.inet_aton(srcip)
    dstip = socket.inet_aton(dstip)
  
    ver = 4     #Version 4 for IPv4
    ihl = 5     #Header length in 32 bit words. 5 words == 20 bytes
    dscp_ecn = 0#Optional fields, don't feel like implementing. Let's keep it at 0
    tlen = datal + 28 #Length of data + 20 bytes for ipv4 header + 8 bytes for udp     header
    ident = socket.htons(54321) #ID of packet
    flg_frgoff = 0 #Flags and fragment offset
    ttl = 64 #Time to live
    ptcl = 17 #Protocol, 17 (UDP)
    chksm = 13701 #Will automatically fill in checksum 

    return struct.pack(
        "!"     #Network(Big endian)
        "2B"    #Version and IHL, DSCP and ECN
        "3H"    #Total Length, Identification, Flags and Fragment Offset
        "2B"    #Time to live, Protocol
        "H"     #Checksum
        "4s"    #Source ip
        "4s"    #Destination ip
        , (ver << 4) + ihl, dscp_ecn, tlen, ident, flg_frgoff, ttl, ptcl, chksm, srcip, dstip)
 

def make_udp_header(srcport, dstport, datal):
    return struct.pack("!4H", srcport, dstport, datal+8, 0)


def make_udp_packet(src, dst, data):
    ph = make_ipv4_header(src[0], dst[0], len(data), src[1], dst[1])
    uh = make_udp_header(src[1], dst[1], len(data))
    return ph+uh+data


if __name__ == '__main__':
    wizfi = WizFi210SerialCmd(COM_PORT, BAUDRATE, 1)
    wizfi.Write_CMD("AT", "[OK]","","", 10)
    
    wizfi.Write_CMD("AT+WD","[OK]","","[ERROR:", 10)
    cmd_str = "AT+WWPA=" + PASSWORD
    wizfi.Write_CMD(cmd_str,"[OK]","","",10)
    wizfi.Write_CMD("AT+NDHCP=1", "[OK]","","",10);
    
    cmd_str = "AT+WA=" + SSID
    wizfi.Write_CMD(cmd_str,"[OK]","","[ERROR]",10)
    
    wizfi.Write_CMD("AT+NRAW=2","[OK]","","[ERROR]",10)
   
    payload = "Hi WizFi250"
    #ip = make_ip(socket.IPPROTO_TCP, SRC_IP, DEST_IP)
    #tcp = make_tcp(SRC_PORT, DEST_PORT, payload)
    #packet = DEST_ADDR + SRC_ADDR + "\x08\x00" +  ip + tcp + payload

    packet = DEST_ADDR + SRC_ADDR + "\x08\x00"
    packet += make_udp_packet((SRC_IP,SRC_PORT),(DEST_IP,DEST_PORT),"Hi WizFi210")

    strlen = len(packet)
    cmd_str = "\x1BR:" + str(strlen) + ":" + packet
    
    for character in cmd_str:
        print("{%c}:{%s}" % (character, character.encode('hex')))

    wizfi.Write_CMD(cmd_str,"","","",10)
    wizfi.Write_CMD(cmd_str,"","","",10)

    wizfi.Write_CMD("AT", "[OK]","","", 10)

    wizfi.serialClose();

