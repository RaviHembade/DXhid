from tb_device_mqtt import TBDeviceMqttClient, TBPublishInfo
import json 

#def parse_msg(msg):
    # print("MSG: ", msg)
    # print(msg.split(";"))
    telemetry = {}
    # msg = "1060;003368;2;20;1;22;220;05:46:52 IST 05/21/2019;00:06:8E:03:57:0B;0;0;0000020F000000000000000000000000"
    if(msg.strip().split(";")[0]=="1060" and msg.strip() != ""):
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
#       telemetry["Interface  Adddress"] = msg.split(";")[9]
#       telemetry["Reader  Adddress"] = msg.split(";")[10]
#       telemetry["Card Number "] = msg.split(";")[11]
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
        # Disconnect from ThingsBoard
        client.disconnect()