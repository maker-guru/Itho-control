#fan control usig mqtt
import paho.mqtt.client as mqtt
import time
import fan

# Configuratie voor de MQTT-broker
BROKER = 'homeassistant.local'
PORT = 1883
TOPIC = 'test/tryit'
Q_USER = 'fan_mqtt'
Q_PSWD = 'FanMQTT4me'
LISTEN_DURATION = 10  # Tijd in seconden dat je wilt luisteren



# Callback voor wanneer de client verbinding maakt met de broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        #print("Verbonden met broker")
        client.subscribe(TOPIC)
    else:
        print("Verbindingsfout, code:", rc)
        print("Code = " + str(rc))
        print("Flags = " + str(flags))
        print("user data = " + str(userdata))

# Callback voor wanneer een bericht wordt ontvangen van het topic
def on_message(client, userdata, msg):
    #print("Ontvangen bericht op topic " + TOPIC + " : " + msg.payload.decode())
    payload = msg.payload.decode()
    if "high" in payload:
        #print("high")
        fan.set_fan_high()
    elif ("medium") in payload:
        #print("medium")
        fan.set_fan_medium()
    elif "low" in payload:
        #print("low")
        fan.set_fan_low()
    elif "off" in payload: 
        print("off")
    
    
    

# MQTT client instellen en verbinden
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(Q_USER, Q_PSWD)

try:
    client.connect(BROKER, PORT)
    start_time = time.time()

    # Luister voor de ingestelde duur
    #while (time.time() - start_time) < LISTEN_DURATION:
    #    client.loop(timeout=1.0)  # Voert de lus met een time-out van 1 seconde uit
    client.loop_forever()

    #print("Luistertijd verstreken, verbinding sluiten")
    client.disconnect()

except KeyboardInterrupt:
    print("Afgesloten door gebruiker")
    client.disconnect()
    