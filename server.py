import socket
import sys
from tb_device_mqtt import TBDeviceMqttClient, TBPublishInfo
import json 

def parse_msg(msg):
    print("MSG: ", msg)
    # print(msg.split(";"))
    telemetry = {}
    # msg = "1060;003368;2;20;1;22;220;05:46:52 IST 05/21/2019;00:06:8E:03:57:0B;0;0;0000020F000000000000000000000000;26"
    if(msg.strip().split(";")[0]=="1060" and msg.strip() != ""):
        if(msg.split(";")[4] == "1" and msg.split(";")[5] == "22" ):
            print("MSG Inside: ", msg)
            telemetry["eventid"] = msg.split(";")[0]
            telemetry["msgid"] = msg.split(";")[1]
            telemetry["eventmessagetype"] = msg.split(";")[2]
            telemetry["classcode"] = msg.split(";")[3]
            telemetry["taskcode"] = msg.split(";")[4]
            telemetry["eventcode"] = msg.split(";")[5]
            telemetry["priority"] = msg.split(";")[6]
            telemetry["msgtime"] = msg.split(";")[7]
            telemetry["macaddr"] = msg.split(";")[8]
            telemetry["Interface  Adddress"] = msg.split(";")[9]
            telemetry["Reader  Adddress"] = msg.split(";")[10]
            telemetry["Card Number "] = msg.split(";")[11]
            telemetry["Card byte "] = msg.split(";")[12]
            # telemetry = {"temperature": 41.9, "enabled": False, "currentFirmwareVersion": "v1.2.2"}
            client = TBDeviceMqttClient("dev.dataexchange.io", "JUSf1I0L3cGBTskcTDgw")
            # Connect to ThingsBoard
            client.connect()
            # Sending telemetry without checking the delivery status
            client.send_telemetry(telemetry) 
            # Sending telemetry and checking the delivery status (QoS = 1 by default)
            result = client.send_telemetry(telemetry)
            # get is a blocking call that awaits delivery status  
            success = result.get() == TBPublishInfo.TB_ERR_SUCCESS
            print("MESSAGE SENT: ", success)
            print(success)
            # Disconnect from ThingsBoard
            client.disconnect()
        elif(msg.strip().split(";")[0]=="1060" and msg.strip() != ""):
            if(msg.split(";")[4] == "2" and msg.split(";")[5] == "20" ):
                print("MSG Inside: ", msg)
                telemetry["eventid"] = msg.split(";")[0]
                telemetry["msgid"] = msg.split(";")[1]
                telemetry["eventmessagetype"] = msg.split(";")[2]
                telemetry["classcode"] = msg.split(";")[3]
                telemetry["taskcode"] = msg.split(";")[4]
                telemetry["eventcode"] = msg.split(";")[5]
                telemetry["priority"] = msg.split(";")[6]
                telemetry["msgtime"] = msg.split(";")[7]
                telemetry["macaddr"] = msg.split(";")[8]
                telemetry["Interface  Adddress"] = msg.split(";")[9]
                telemetry["Reader  Adddress"] = msg.split(";")[10]
                telemetry["Card Number "] = msg.split(";")[11]       
                # telemetry = {"temperature": 41.9, "enabled": False, "currentFirmwareVersion": "v1.2.2"}
                client = TBDeviceMqttClient("dev.dataexchange.io", "JUSf1I0L3cGBTskcTDgw")
                # Connect to ThingsBoard
                client.connect()
                # Sending telemetry without checking the delivery status
                client.send_telemetry(telemetry) 
                # Sending telemetry and checking the delivery status (QoS = 1 by default)
                result = client.send_telemetry(telemetry)
                # get is a blocking call that awaits delivery status  
                success = result.get() == TBPublishInfo.TB_ERR_SUCCESS
                print("MESSAGE SENT: ", success)
                print(success)
                # Disconnect from ThingsBoard
                client.disconnect()

def recvall(sock):
    BUFF_SIZE = 4096 # 4 KiB
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            # either 0 or end of data
            break
    return data


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('0.0.0.0', 4070)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            # data = connection.recv(10240)
            data = recvall(connection)
            if(data.strip() != ""):
                print('received {!r}'.format(data))
                print('Data List: \n')
                dlst = str(data.decode()).split("^")
                # dlst = [x for x in dlst if "1060;" in x]
                if("" in dlst):
                    dlst.remove("")
                    print("Last element of list:", dlst[-1])
                    parse_msg(dlst[-1])
                    if data:
                        print('sending data back to the client')
                        #connection.sendall(data)

                    print('no data from', client_address)
                    break            

    finally:
        # Clean up the connection
        connection.close()