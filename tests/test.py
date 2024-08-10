import unittest
from ttn_client import TTN_client
from secret import SECRET

# EXAMPLE: 
# Client configuration
ttn_version = "v3" # string
ttn_version = TTN_client.VERSION.V3 # predefined string

network_cluster = "eu1" # string
network_cluster = TTN_client.NETWORK_CLUSTER.EU1 # predefined string

# Secret parameters
app_id = SECRET["app_id"]
api_key = SECRET["api_key"]
app_key = SECRET["app_key"]

# Client initialization
client = TTN_client(network_cluster, ttn_version, app_id, api_key, app_key)

# Display Client configuration
print(f"TTN Client: \n {client.info()}")

# Client devices
print(f"GET devices: \n {client.devices()}")

# Get device by device_id
print(f"DEVICE: \n {client.device("first-end-device")}")

# Register new device: OTAA
test_dev_id = "second-end-device"
test_dev_eui = SECRET["dev_eui"]
response = client.otaa(test_dev_id, test_dev_eui, "0000000000000000")
print(f"OTAA: \n {response} \n {response.json()}")

# Delete device from application
response = client.delete_device(test_dev_id)
print(f"Device deletion: \n {response}")

