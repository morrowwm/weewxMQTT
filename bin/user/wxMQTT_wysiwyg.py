#!/usr/bin/python
#
# weewx driver that reads data from MQTT subscription
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.
#
# See http://www.gnu.org/licenses/

#
# The units must be weewx.US:   (this comment need to be updated)
#   degree_F, inHg, inch, inch_per_hour, mile_per_hour
#
# To use this driver, put this file in the weewx user directory, then make
# the following changes to weewx.conf:
#
# [Station]
#     station_type = wxMesh
# [wxMesh]
#     host = localhost           # MQTT broker hostname
#     topic = weather            # topic, mqtt topics should have format "topic/label_map", ex: weather/humi
#     driver = user.wxMesh
#
# If the variables in the file have names different from those in weewx, then
# create a mapping such as this:
#
# [wxMesh]
#     ...
#     [[label_map]]
#         temp = outTemp
#         humi = outHumidity
#         in_temp = inTemp
#         in_humid = inHumidity

from __future__ import with_statement
import syslog
import time
import paho.mqtt.client as mqtt
import weewx.drivers

DRIVER_VERSION = "0.1"

def logmsg(dst, msg):
    syslog.syslog(dst, 'wxMesh: %s' % msg)

def logdbg(msg):
    logmsg(syslog.LOG_DEBUG, msg)

def loginf(msg):
    logmsg(syslog.LOG_INFO, msg)

def logerr(msg):
    logmsg(syslog.LOG_ERR, msg)

def _get_as_float(d, s):
    v = None
    if s in d:
        try:
            v = float(d[s])
        except ValueError, e:
            logerr("cannot read value for '%s': %s" % (s, e))
    return v

def loader(config_dict, engine):
    return wxMesh(**config_dict['wxMesh'])

class wxMesh(weewx.drivers.AbstractDevice):
    """weewx driver that reads data from a file"""

    def __init__(self, **stn_dict):
        # where to find the data file
        self.host = stn_dict.get('host', 'localhost')
        # subscribe to all sub-topic of the topic define in weewx.conf 
        self.topic = stn_dict.get('topic', 'weather') + "/#"
	self.username = stn_dict.get('username', 'default_usernameXXX')
        self.password = stn_dict.get('password', 'password')
	self.clientid = stn_dict.get('client', 'weewx_mqttc')
        # how often to poll the weather data file, seconds
        self.poll_interval = float(stn_dict.get('poll_interval', 5.0))
        # mapping from variable names to weewx names
        self.label_map = stn_dict.get('label_map', {})

        loginf("host is %s" % self.host)
        loginf("topic is %s" % self.topic)
        loginf("polling interval is %s" % self.poll_interval)
        loginf('label map is %s' % self.label_map)
        self.payload = "Empty"
	self.receive_buffer = {}
        #self.payloadList = [payload]
        self.client = mqtt.Client(client_id=self.clientid, protocol=mqtt.MQTTv31)

	#self.client.on_connect = self.on_connect
	self.client.on_message = self.on_message

        self.client.username_pw_set(self.username, self.password)
	self.client.connect(self.host, 1883, 60)
	self.client.subscribe(self.topic, qos=0)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
	self.payload = str(msg.payload)
	string_topic = str(msg.topic)
	key =  string_topic.split('/')[-1] 
        self.receive_buffer[key] = str(msg.payload)

    def closePort(self):
	self.client.loop_stop()
        self.client.disconnect()

    def genLoopPackets(self):
        self.client.loop_start()   # enable to receive ('on_message') in background
        while True:
            time.sleep(self.poll_interval) # wait for some MQTT data to be published
            data = self.receive_buffer.copy()
            self.receive_buffer.clear()
            if data:       # if data is not empty then prepare loop packet
                _packet = {'dateTime': int(time.time() + 0.5),'usUnits': weewx.METRIC}
                logdbg("dateTime %s" % _packet["dateTime"])
                for vname in data:
                    _packet[self.label_map.get(vname, vname)] = _get_as_float(data, vname)
                    logdbg("packet content: %s =  %s" %(self.label_map.get(vname, vname), data[vname]))
                yield _packet
                data.clear()
#	self.client.loop_stop()

    @property
    def hardware_name(self):
        return "wxMesh"
