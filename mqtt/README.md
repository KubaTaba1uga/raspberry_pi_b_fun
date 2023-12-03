# MQTT overview

MQTT is sub-pub protocol. 
It's commonly used in IOT cause of it's light weight and simplicity.

# Mosquito

Eclipse Mosquito is open-source MQTT server implementation.

## Subscribing a topic

```
mosquitto_sub -v -h localhost -t 'iot'
```

## Publishing a message
```
mosquitto_pub -v -h localhost -t 'iot' -m 'Client 0: hello world'
```

## Topics and wildcards 

`+` is used to match a single elemnt of the jierarchy
`#` is used to match all remaining elements of the hierarchy.

`+/+/lighting/+` matches `level1/lounge/lighting/sensor1`

## QoS

Level 0 - The message will be delivered at most once but maybe not at all.
Level 1 - The message will be delivered at least once but perhaps more.
Level 2 - The message will be delivered exactly once.

QoS levels apply to message subscription and message publishing.
One client may publish a messate to a topic with QoS 1, another one may subscribe to the same topic with QoS 2.

The delvery QoS received by a client is downgraded to the lowest QoS of the publications or subscription.
For example: Publisher QoS 1, Subscriber QoS 0, Delivery QoS 0

We can subscribe or publish adding 
```
-q <level>
```
Example:
```
mosquitto_sub -v -h localhost -t 'iot' -q 0
```

Try publishing and subscribing with different QoS. Adding `-d` flag allows You how clients downgrade QoS.

## Retaining messages
All messages may be set to be retained. This means that the broker will keep the message even after sending it to 
all current subscribers. If a new subscription is made that matches the topic of the retained message, then the
message will be sent to the client. This is useful as a "last known good" mechanism. If a topic is only updated 
infrequently, then without a retained message, a newly subscribed client may have to wait a long time to receive
an update. With a retained message, the client will receive an instant update.

We can publish adding 
```
-r
```
Example:
```
mosquitto_pub -v -h localhost -t 'iot' -r -m 'hello world'
```


## Durable connections 
On connection, a client sets the "clean session" flag, which is sometimes also known as the "clean start" flag.
If clean session is set to false, then the connection is treated as durable. This means that when the client
disconnects, any subscriptions it has will remain and any subsequent QoS 1 or 2 messages will be stored until it
connects again in the future. If clean session is true, then all subscriptions will be removed for the client when
it disconnects.

We can subscribe adding 
```
-i <client id>
-c 
```

Client id is a unique client ID (this is how the broker identifies the client).
`-c` tells the broker to disable session cleanup.

Example:
```
mosquitto_sub -v -h localhost -t 'iot' -c -i abababababv
```

Durable connection require QoS > 0.

## Will

Subscriber can post a Will, will is a message that will be sent to other subscribers/publishers, when it's creator
becomes unavailable. 

Rfc:
```
DISCONNECT
  The DISCONNECT packet is the final MQTT Control Packet sent from the Client or the
  Broker. It indicates the reason why the Network Connection is being closed. If the
  Network Connection is closed without the Client first sending a DISCONNECT packet
  with reason code 0x00 (Normal disconnection) and the MQTT Connection has a Will
  Message, the Will Message is published.
```

