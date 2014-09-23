ScriptForUsingRawPacketOnWizFi210
=================================

This is python script for using raw packet on WizFi210
####1. Check Firmware & Hardware version of WizFi210/220####
For using this function, WizFi210/220 must have firmware more 1.2.0.3(S2WEAP). This firmware can be uploaded from the hardware version 1.0.1.

####2. Test Environment ####
This example explain How to use sending Raw Packet on WizFi210. So I will send "Hi WizFi210 " message using Raw packet on WizFi210 to PC.
This picture is test environment.

![WizFi210_Raw_Packet3](https://raw.githubusercontent.com/Wiznet/ScriptForUsingRawPacketOnWizFi210/master/image/WizFi210_Raw_Packet3.png "WizFi210_Raw_Packet3")


###3. AT Command Set of WizFi210 ###
```
AT
[OK]

AT+WD
[OK]

AT+WWPA=qazxswedc
[OK]

AT+NDHCP=1
[OK]

AT+WA=WiznetKaizen
    IP              SubNet         Gateway   
 192.168.201.21: 255.255.255.0: 192.168.201.1 
[OK]

AT+NRAW=2
[OK]

<Esc>R:<Length>:<DstAddr><SrcAddr><EtherType><Raw-Payload>
```
Length is size of DstAddr, SrcAddr, EtherType and Payload.


###4. Python Script for sending raw packet on WizFi210###
you can download python script at this URL.
[https://github.com/Wiznet/ScriptForUsingRawPacketOnWizFi210](https://github.com/Wiznet/ScriptForUsingRawPacketOnWizFi210)

###5. Screenshot when receive packet on PC###

![WizFi210_Raw_Packet1](https://raw.githubusercontent.com/Wiznet/ScriptForUsingRawPacketOnWizFi210/master/image/WizFi210_Raw_Packet1.png "WizFi210_Raw_Packet1")
![WizFi210_Raw_Packet2](https://github.com/Wiznet/ScriptForUsingRawPacketOnWizFi210/blob/master/image/WizFi210_Raw_Packet2.png "WizFi210_Raw_Packet2")
