# installer for the weewxMQTT driver
#
# Based on installer for bootstrap skin
#
# Configured by Bill to install weewxMQTT user driver, 2016.

import os.path
import configobj

import setup
import distutils

def loader():
    return weewxMQTTInstaller()

class weewxMQTTInstaller(setup.ExtensionInstaller):
    _driver_conf_files = ['weewx.conf']

    def __init__(self):
        super(weewxMQTTInstaller, self).__init__(
            version="0.2",
            name='weewxMQTT',
            description='A weewx driver which subscribes to MQTT topics providing weewx compatible data',
            author="Bill Morrow",
            author_email="morrowwm@gmail.com",
            config={
                'wxMesh': {
                    driver = user.wxMesh
                    host = localhost           # MQTT broker hostname
                    topic = weather            # topic
                    poll_interval = 1
    
                    [[label_map]]
                    TIME = dateTime
                    HUMT = outTemp
                    RHUM = outHumidity
                    INTE = inTemp
                    INHU = inHumidity
                    BARP = barometer
                    IRRA = radiation
                    PHOV = supplyVoltage
                    BATV = consBatteryVoltage
                    AMBT = extraTemp1
                    SYST = extraTemp2
                    WDIR = windDir
                    WIND = windSpeed
                 }

            files=[('bin/users/wxMesh'])]
            )

        print ""
        print "The following alternative languages are available:"
        self.language = None

    def merge_config_options(self):

        fn = os.path.join(self.layout['CONFIG_ROOT'], 'weewx.conf')
        config = configobj.ConfigObj(fn)
