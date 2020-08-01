<h1>
  <a href='http://www.weewx.com'>WeeWX</a>
</h1>
<p><i>Open source software for your weather station</i></p>

<h2>Description</h2>
<p>This version is compatible Python3 et Weewx 4.1.x</p>
<p>An extension of weewx to add a driver which gets data via an MQTT subscription. Also will shortly add the software from the other side of the MQTT broker. Main part of that is an RF24Mesh process.
</p>

<p>Works well with the <a href='https://mosquitto.org/'>Mosquitto</a> MQTT message broker.</p>
<h2>Features</h2>
<ul>
  <li>If a message provides 0 as the timestamp or does not provide a timestamp, the driver uses the time on the weewx host.</li>
  <li>Consolidates asynchronous readings from more than one device into one stream of periodic weewx records.</li>
  <li>Queues fast arriving publications and processes them into weewx packets quickly, then sleeps.</li>
</ul>

<h2>Downloads</h2>

<p>
For current and previous releases:
</p>
<p>
<a href='https://github.com/morrowwm/weewxMQTT'>https://github.com/morrowwm/weewxMQTT</a>
</p>

<h2>Installation</h2>
<p>
Install paho MQTT client using
    sudo pip3 install paho-mqtt
</p>
<h2>Documentation and Support</h2>

<p>
The github project's <a href='https://github.com/morrowwm/weewxMQTT/wiki'>wiki</a>.

<p>
  Community support for weewx can be found at:
<p style='padding-left: 50px;'>
  <a href="https://groups.google.com/group/weewx-user">https://groups.google.com/group/weewx-user</a>
</p>

<h2>Licensing</h2>

<p>weewxMQTT is licensed under the GNU Public License v3.</p>
