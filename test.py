from ttn import TTN_client

ttn = "v3"
ttn = TTN_client.VERSION.V3
network_cluster = "eu1"
network_cluster = TTN_client.NETWORK_CLUSTER.EU1
# network_cluster = TTN_client.NETWORK_CLUSTER.EU1
app_id = "python-dev-management"
api_key = "NNSXS.BQYNOFOCDRBYAPXIJFJRHKFQOR6YGTFVQJDNV5A.MAYM5YPUBIRJIEOOL2XLJI6GY5WCKP6GSYUOJDMMNG64WH2B26MQ"
app_key = "4868DC1E6296C0A329A2287BF06B5BA9"

client = TTN_client(network_cluster, ttn, app_id, api_key, app_key)
print(client.list_attributes())
print(client)

# print("GET Devices:")
# response = client.get_devices()
# print(response)

# print("GET device by id")
# device_id = "first-end-device"
# response = client.get_device(device_id)
# print(response)

# print("Delete end-device from IS: \n\n")
# response = client.delete_IS("second-end-device")
# print(response)

# response = client.register_IS("second-end-device", "70B3D57ED0069759", "0000000000000000")
# print(response, response.json())

# response = client.register_JS("second-end-device", "70B3D57ED0069759", "0000000000000000")
# print(response, response.json())

# response = client.register_NS("second-end-device", "70B3D57ED0069759", "0000000000000000")
# print(response, response.json())

# response = client.register_AS("second-end-device", "70B3D57ED0069759", "0000000000000000")
# print(response, response.json())



# response = client.otaa("second-end-device", "70B3D57ED0069759", "0000000000000000")
# print(response, response.json())
# 
# response = client.delete_end_device("second-end-device")
# print(response, response.json())

# client.api_key = "s"