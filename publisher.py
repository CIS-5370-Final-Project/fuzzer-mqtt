import json
import time
from datetime import datetime

import paho.mqtt.client as mqtt

# MQTT Broker configuration
MQTT_BROKER = "mosquitto"
MQTT_PORT = 1883
MQTT_TOPIC = "test/topic"
MQTT_CLIENT_ID = "publisher-client"


def on_connect(client, userdata, flags, rc):
    """Callback when client connects to broker"""
    if rc == 0:
        print(f"[{datetime.now()}] Connected to MQTT Broker successfully")
    else:
        print(f"[{datetime.now()}] Failed to connect, return code {rc}")


def on_publish(client, userdata, mid):
    """Callback when message is published"""
    print(f"[{datetime.now()}] Message published (mid: {mid})")


def main():
    # Create MQTT client
    client = mqtt.Client(client_id=MQTT_CLIENT_ID)

    # Set callbacks
    client.on_connect = on_connect
    client.on_publish = on_publish

    # Connect to broker
    print(f"[{datetime.now()}] Connecting to MQTT Broker at {MQTT_BROKER}:{MQTT_PORT}")
    client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)

    # Start network loop in background
    client.loop_start()

    # Wait for connection
    time.sleep(2)

    # Publish messages continuously
    message_count = 0
    try:
        while True:
            message_count += 1

            # Create message payload
            payload = {
                "message_id": message_count,
                "timestamp": datetime.now().isoformat(),
                "data": f"Hello from publisher #{message_count}",
                "sensor_data": {
                    "temperature": 20 + (message_count % 10),
                    "humidity": 50 + (message_count % 20),
                },
            }

            # Convert to JSON
            message = json.dumps(payload)

            # Publish message
            result = client.publish(MQTT_TOPIC, message, qos=1)

            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"[{datetime.now()}] Published: {message}")
            else:
                print(f"[{datetime.now()}] Failed to publish message")

            # Wait before publishing next message
            time.sleep(5)

    except KeyboardInterrupt:
        print(f"\n[{datetime.now()}] Publisher stopped by user")
    finally:
        client.loop_stop()
        client.disconnect()
        print(f"[{datetime.now()}] Disconnected from broker")


if __name__ == "__main__":
    main()
