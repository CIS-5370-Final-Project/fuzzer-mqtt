from boofuzz import (
    Session,
    SocketConnection,
    Target,
    s_block_end,
    s_block_start,
    s_byte,
    s_get,
    s_initialize,
    s_size,
    s_static,
    s_string,
    s_word,
)

# Configure target MQTT broker
MQTT_HOST = "localhost"
MQTT_PORT = 1883

# Create session with logging and crash detection
session = Session(
    target=Target(connection=SocketConnection(MQTT_HOST, MQTT_PORT, proto="tcp")),
    sleep_time=0.1,
    receive_data_after_fuzz=True,
    check_data_received_each_request=False,
)

# ============================================================================
# MQTT CONNECT Packet
# ============================================================================
s_initialize("mqtt_connect")

# Fixed Header
s_byte(0x10, name="packet_type", fuzzable=False)  # CONNECT packet type
s_size(
    "connect_body", length=1, math=lambda x: x, name="remaining_length", fuzzable=True
)

if s_block_start("connect_body"):
    # Variable Header - Protocol Name
    s_word(0x0004, name="protocol_name_len", endian=">", fuzzable=True)
    s_static("MQTT", name="protocol_name_str")

    # Protocol Level & Flags
    s_byte(0x04, name="protocol_level", fuzzable=True)  # MQTT 3.1.1
    s_byte(0x02, name="connect_flags", fuzzable=True)  # Clean session flag
    s_word(60, name="keep_alive", endian=">", fuzzable=True)

    # Payload - Client ID
    s_word(0x000D, name="client_id_len", endian=">", fuzzable=True)
    s_string("fuzzed_client", name="client_id", fuzzable=True)

s_block_end()

# ============================================================================
# MQTT SUBSCRIBE Packet
# ============================================================================
s_initialize("mqtt_subscribe")

# Fixed Header
s_byte(0x82, name="packet_type", fuzzable=False)  # SUBSCRIBE packet type with QoS 1
s_size(
    "subscribe_body", length=1, math=lambda x: x, name="remaining_length", fuzzable=True
)

if s_block_start("subscribe_body"):
    # Variable Header - Packet ID
    s_word(0x0001, name="packet_id", endian=">", fuzzable=True)

    # Payload - Topic filter
    s_word(0x000A, name="topic_len", endian=">", fuzzable=True)
    s_string("test/topic", name="topic_filter", fuzzable=True)
    s_byte(0x00, name="qos", fuzzable=True)  # Requested QoS

s_block_end()

# ============================================================================
# MQTT PUBLISH Packet
# ============================================================================
s_initialize("mqtt_publish")

# Fixed Header
s_byte(0x30, name="packet_type", fuzzable=True)  # PUBLISH, QoS 0
s_size(
    "publish_body", length=1, math=lambda x: x, name="remaining_length", fuzzable=True
)

if s_block_start("publish_body"):
    # Variable Header - Topic Name
    s_word(0x000A, name="topic_len", endian=">", fuzzable=True)
    s_string("test/topic", name="topic", fuzzable=True)

    # Payload - Message
    s_string("fuzzed_payload_data", name="message", fuzzable=True, max_len=1000)

s_block_end()

# ============================================================================
# MQTT PINGREQ Packet
# ============================================================================
s_initialize("mqtt_pingreq")
s_byte(0xC0, name="packet_type", fuzzable=False)
s_byte(0x00, name="remaining_length", fuzzable=True)

# ============================================================================
# MQTT DISCONNECT Packet
# ============================================================================
s_initialize("mqtt_disconnect")
s_byte(0xE0, name="packet_type", fuzzable=False)
s_byte(0x00, name="remaining_length", fuzzable=True)

# ============================================================================
# Define fuzzing graph
# ============================================================================
session.connect(s_get("mqtt_connect"))
session.connect(s_get("mqtt_connect"), s_get("mqtt_subscribe"))
session.connect(s_get("mqtt_connect"), s_get("mqtt_publish"))
session.connect(s_get("mqtt_connect"), s_get("mqtt_pingreq"))
session.connect(s_get("mqtt_connect"), s_get("mqtt_disconnect"))

# Start fuzzing
print(f"Starting MQTT fuzzing session against {MQTT_HOST}:{MQTT_PORT}")
print("Press Ctrl+C to stop fuzzing")
session.fuzz()
