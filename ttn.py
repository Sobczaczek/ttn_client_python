import requests
import json



class TTN_client:
    def __init__(self, network_cluster, app_id, api_key):
        self.network_cluster = network_cluster
        self.base_url = f"https://{network_cluster}/api/v3/applications/{app_id}"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def get_devices(self):
        """
        Get the list of devices registered on your app.
        """
        url = f"{self.base_url}/devices"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_device(self, device_id):
        """
        @note   Get details of specific device
        @param  dev_id - unique device identifier 
        """
        url = f"{self.base_url}/devices/{device_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    # def send_downlink(self, dev_id, payload):
        # """
        # Downlink to the end-device.
        # """
        # url = f"{self.base_url}/devices/{dev_id}/down"
 
    # def receive_uplink(self, dev_id):
        # pass
    
    def register_IS(self, device_id, dev_eui, join_eui):
        """Register a device in the Identity Server."""
        data = {
            "end_device": {
                "ids": {
                    "device_id": device_id,
                    "dev_eui": dev_eui,
                    "join_eui": join_eui
                },
                "join_server_address": self.network_cluster,
                "network_server_address": self.network_cluster,
                "application_server_address": self.network_cluster
            },
            "field_mask": {
                "paths": [
                    "join_server_address",
                    "network_server_address",
                    "application_server_address",
                    "ids.dev_eui",
                    "ids.join_eui"
                ]
            }
        }
        url = f"{self.base_url}/devices"
        response = requests.post(url, data=json.dumps(data), headers=self.headers)
        response.raise_for_status()
        return response
