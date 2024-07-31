from ttn import TTN_client

# params
app_id = "python-dev-management"
api_key = "NNSXS.QYUHLUNUDFXZ6JH7TZ34PNTQUMD5M42FAYZT7JA.PPDFZHIOZP3VT6WARE2MXXC7IMPVGTBD45EV6EHIG3Q7PY7JB7YQ"
net_cluster = "eu1.cloud.thethings.network"

# client
client = TTN_client(net_cluster, app_id, api_key)

# test: get devices
# devices = client.get_devices()
# print("Devices:", devices)

# test: get device
dev_id = "first-end-device"
# device = client.get_device(device_id=dev_id)
# print("Device:", device)

# test: register in IS
dev_id = "third-end-device"
dev_eui = "70B3D57ED0069758"
join_eui = "0000000000000000"

response = client.register_IS(dev_id, dev_eui, join_eui)
print("IS:", response.json())