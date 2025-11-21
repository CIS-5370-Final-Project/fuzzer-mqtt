import json
from datetime import datetime

import paho.mqtt.client as mqtt

# MQTT Broker configuration
MQTT_BROKER = "mosquitto"
MQTT_PORT = 1883
MQTT_TOPIC = "test/topic"
MQTT_CLIENT_ID = "subscriber-client"


def on_connect(client, userdata, flags, rc):
    """Callback when client connects to broker"""
    if rc == 0:
        print(f"[{datetime.now()}] Connected to MQTT Broker successfully")
        # Subscribe to topic after successful connection
        client.subscribe(MQTT_TOPIC, qos=1)
        print(f"[{datetime.now()}] Subscribed to topic: {MQTT_TOPIC}")
    else:
        print(f"[{datetime.now()}] Failed to connect, return code {rc}")


def on_message(client, userdata, msg):
    """Callback when message is received"""
    print(f"\n[{datetime.now()}] Message received on topic: {msg.topic}")
    print(f"QoS: {msg.qos}")
    print(f"Retain: {msg.retain}")

    try:
        # Try to parse as JSON
        payload = json.loads(msg.payload.decode())
        print("Payload (JSON):")
        print(json.dumps(payload, indent=2))
    except json.JSONDecodeError:
        # If not JSON, print raw payload
        print(f"Payload (raw): {msg.payload.decode()}")
    print("-" * 60)


def on_subscribe(client, userdata, mid, granted_qos):
    """Callback when subscription is confirmed"""
    print(f"[{datetime.now()}] Subscription confirmed (mid: {mid}, QoS: {granted_qos})")


def on_disconnect(client, userdata, rc):
    """Callback when client disconnects"""
    if rc != 0:
        print(f"[{datetime.now()}] Unexpected disconnection. RC: {rc}")


def main():
    # Create MQTT client
    client = mqtt.Client(client_id=MQTT_CLIENT_ID)

    # Set callbacks
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = on_subscribe
    client.on_disconnect = on_disconnect

    # Connect to broker
    print(f"[{datetime.now()}] Connecting to MQTT Broker at {MQTT_BROKER}:{MQTT_PORT}")
    client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)

    # Start network loop (blocking)
    print(f"[{datetime.now()}] Waiting for messages... (Press Ctrl+C to stop)")
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print(f"\n[{datetime.now()}] Subscriber stopped by user")
        client.disconnect()
        print(f"[{datetime.now()}] Disconnected from broker")


if __name__ == "__main__":
    main()
