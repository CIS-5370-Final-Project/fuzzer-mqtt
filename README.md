# Mosquitto MQTT Client Usage Guide

## Overview

This guide provides instructions for installing and using Mosquitto MQTT clients on Ubuntu to connect to an MQTT broker.

**Broker Connection Details:**
- **Broker IP:** 104.131.126.29
- **Port:** 1883
- **Protocol:** MQTT (non-secure)

---

## Installation

### Install Mosquitto Clients on Ubuntu

```bash
sudo apt update
sudo apt install mosquitto-clients -y
```

### Verify Installation

```bash
mosquitto_pub --help
mosquitto_sub --help
```

---

## Basic Usage

### Subscribe to a Topic

Subscribe to receive messages from a specific topic:

```bash
mosquitto_sub -h 104.131.126.29 -p 1883 -t "test/topic"
```

**Options:**
- `-h` : Broker hostname or IP address
- `-p` : Port number
- `-t` : Topic to subscribe to

### Publish a Message

Send a message to a specific topic:

```bash
mosquitto_pub -h 104.131.126.29 -p 1883 -t "test/topic" -m "Hello MQTT!"
```

**Options:**
- `-h` : Broker hostname or IP address
- `-p` : Port number
- `-t` : Topic to publish to
- `-m` : Message payload

---

## Advanced Usage

### Subscribe to Multiple Topics

```bash
mosquitto_sub -h 104.131.126.29 -p 1883 -t "sensor/temperature" -t "sensor/humidity"
```

### Subscribe to All Topics (Wildcard)

```bash
# Subscribe to all topics
mosquitto_sub -h 104.131.126.29 -p 1883 -t "#"

# Subscribe to all topics under a specific path
mosquitto_sub -h 104.131.126.29 -p 1883 -t "sensor/#"
```

### Publish with QoS (Quality of Service)

```bash
# QoS 0 (At most once - default)
mosquitto_pub -h 104.131.126.29 -p 1883 -t "test/topic" -m "QoS 0 message" -q 0

# QoS 1 (At least once)
mosquitto_pub -h 104.131.126.29 -p 1883 -t "test/topic" -m "QoS 1 message" -q 1

# QoS 2 (Exactly once)
mosquitto_pub -h 104.131.126.29 -p 1883 -t "test/topic" -m "QoS 2 message" -q 2
```

### Retain Messages

Publish a message that will be retained by the broker:

```bash
mosquitto_pub -h 104.131.126.29 -p 1883 -t "status/device" -m "online" -r
```

The `-r` flag marks the message as retained. New subscribers will immediately receive the last retained message.

### Subscribe with Verbose Output

```bash
mosquitto_sub -h 104.131.126.29 -p 1883 -t "test/topic" -v
```

The `-v` flag shows the topic name along with the message.

### Publish JSON Data

```bash
mosquitto_pub -h 104.131.126.29 -p 1883 -t "sensor/data" -m '{"temperature":22.5,"humidity":65}'
```

### Publish from File

```bash
mosquitto_pub -h 104.131.126.29 -p 1883 -t "data/file" -f message.txt
```

---

## Client ID

Specify a custom client ID for the connection:

```bash
mosquitto_sub -h 104.131.126.29 -p 1883 -t "test/topic" -i "my-client-id"
```

---

## Keep Alive

Set the keep alive interval (in seconds):

```bash
mosquitto_sub -h 104.131.126.29 -p 1883 -t "test/topic" -k 60
```

---

## Testing Examples

### Example 1: Simple Publish/Subscribe Test

**Terminal 1 (Subscribe):**
```bash
mosquitto_sub -h 104.131.126.29 -p 1883 -t "test/hello" -v
```

**Terminal 2 (Publish):**
```bash
mosquitto_pub -h 104.131.126.29 -p 1883 -t "test/hello" -m "Hello from Ubuntu!"
```

### Example 2: Sensor Data Simulation

**Subscribe to sensor data:**
```bash
mosquitto_sub -h 104.131.126.29 -p 1883 -t "sensor/#" -v
```

**Publish sensor readings:**
```bash
mosquitto_pub -h 104.131.126.29 -p 1883 -t "sensor/temperature" -m "23.5"
mosquitto_pub -h 104.131.126.29 -p 1883 -t "sensor/humidity" -m "67.2"
mosquitto_pub -h 104.131.126.29 -p 1883 -t "sensor/pressure" -m "1013.25"
```

### Example 3: Status Updates with Retained Messages

**Publish device status (retained):**
```bash
mosquitto_pub -h 104.131.126.29 -p 1883 -t "device/status" -m "online" -r
```

**Subscribe to device status:**
```bash
mosquitto_sub -h 104.131.126.29 -p 1883 -t "device/status" -v
```

---

## Common Options Reference

| Option | Description |
|--------|-------------|
| `-h` | Broker hostname/IP address |
| `-p` | Port number (default: 1883) |
| `-t` | Topic |
| `-m` | Message payload (publish only) |
| `-f` | Read message from file (publish only) |
| `-u` | Username for authentication |
| `-P` | Password for authentication |
| `-i` | Client ID |
| `-q` | QoS level (0, 1, or 2) |
| `-r` | Retain message (publish only) |
| `-v` | Verbose output (subscribe only) |
| `-k` | Keep alive interval in seconds |
| `-c` | Clean session (default: true) |
| `-d` | Enable debug messages |

---

## Wildcard Characters

- `+` : Single-level wildcard (e.g., `sensor/+/temperature`)
- `#` : Multi-level wildcard (e.g., `sensor/#`)

**Examples:**
```bash
# Subscribe to all temperature sensors
mosquitto_sub -h 104.131.126.29 -p 1883 -t "sensor/+/temperature"

# Subscribe to all topics under sensor
mosquitto_sub -h 104.131.126.29 -p 1883 -t "sensor/#"
```

---

## Troubleshooting

### Connection Refused

If you get a connection error:
1. Check if the broker is running and accessible
2. Verify the IP address and port are correct
3. Check firewall rules

```bash
# Test network connectivity
ping 104.131.126.29

# Test if port is open
nc -zv 104.131.126.29 1883
```

### Authentication Failed

If authentication fails:
1. Verify username and password are correct
2. Check if the broker requires authentication
3. Ensure the user has appropriate permissions

---

## Additional Resources

- [Mosquitto Documentation](https://mosquitto.org/documentation/)
- [MQTT Protocol Specification](https://mqtt.org/)
- [MQTT Topic Best Practices](https://www.hivemq.com/blog/mqtt-essentials-part-5-mqtt-topics-best-practices/)

---

## Quick Reference Commands

```bash
# Subscribe to a topic
mosquitto_sub -h 104.131.126.29 -p 1883 -t "your/topic"

# Publish a message
mosquitto_pub -h 104.131.126.29 -p 1883 -t "your/topic" -m "your message"

# Subscribe to all topics
mosquitto_sub -h 104.131.126.29 -p 1883 -t "#" -v

# Publish with QoS 1
mosquitto_pub -h 104.131.126.29 -p 1883 -t "your/topic" -m "important message" -q 1

# Publish retained message
mosquitto_pub -h 104.131.126.29 -p 1883 -t "status" -m "online" -r
```

---

**Created:** November 2025  
**Broker:** 104.131.126.29:1883