import requests
import json



class TTN_client:
    def __init__(self, network_cluster, ttn_version, app_id, api_key, app_key):
        self.app_key = app_key
        self.version = ttn_version
        self.app_id = app_id
        self.api_key = api_key
        self.network_cluster = network_cluster
        self.base_url = f"https://{network_cluster}/api/{ttn_version}/"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def get_devices(self) -> requests.Response.json:
        """GET device list from TTN.

        Returns:
            requests.Response.json: list of end-devices, JSON Object
        """
        url = f"{self.base_url}applications/{self.app_id}/devices"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    
    def get_device(self, device_id: str) -> requests.Response.json:
        """_summary_

        Args:
            device_id (str): unique in application device identifier

        Returns:
            requests.Response.json: device information in JSON object
        """
        url = f"{self.base_url}applications/{self.app_id}/devices/{device_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
        
    def register_IS(self, device_id: str, dev_eui: str, join_eui: str) -> requests.Response:
        """_summary_

        Args:
            device_id (str): _description_
            dev_eui (str): _description_
            join_eui (str): _description_

        Returns:
            requests.Response: _description_
        """
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
        url = f"{self.base_url}applications/{self.app_id}/devices"
        response = requests.post(url, data=json.dumps(data), headers=self.headers)
        response.raise_for_status()
        return response
    
    
    def delete_IS(self, device_id: str) -> requests.Response:
        
        url = f"{self.base_url}applications/{self.app_id}/devices/{device_id}"
        response = requests.delete(url, headers=self.headers)
        return response


    def register_JS(self, device_id: str, dev_eui: str, join_eui: str):
        data = {
            "end_device": {
                "ids": {
                "device_id": device_id,
                "dev_eui": dev_eui,
                "join_eui": join_eui
                },
                "network_server_address": self.network_cluster,
                "application_server_address": self.network_cluster,
                "root_keys": {
                "app_key": {
                    "key": self.app_key
                }
                }
            },
            "field_mask": {
                "paths": [
                "network_server_address",
                "application_server_address",
                "ids.device_id",
                "ids.dev_eui",
                "ids.join_eui",
                "root_keys.app_key.key"
                ]
            }
        }
        url = f"{self.base_url}js/applications/{self.app_id}/devices/{device_id}"
        response = requests.put(url, data=json.dumps(data), headers=self.headers)
        response.raise_for_status()
        return response
    
    def delete_JS(self, device_id: str):
        # TODO 
        pass
    
    
    def register_NS(self, device_id: str, dev_eui: str, join_eui: str, lorawan_version="1.0.2", lorawan_phy_version="1.0.2-b", frequency_plan_id="EU_863_870_TTN"):
        data = {
            "end_device": {
                "supports_join": True,
                "lorawan_version": lorawan_version,
                "ids": {
                "device_id": device_id,
                "dev_eui": dev_eui,
                "join_eui": join_eui
                },
                "lorawan_phy_version": lorawan_phy_version,
                "frequency_plan_id": frequency_plan_id
            },
            "field_mask": {
                "paths": [
                "supports_join",
                "lorawan_version",
                "ids.device_id",
                "ids.dev_eui",
                "ids.join_eui",
                "lorawan_phy_version",
                "frequency_plan_id"
                ]
            }
        }
        url = f"{self.base_url}ns/applications/{self.app_id}/devices/{device_id}"
        response = requests.put(url, data=json.dumps(data), headers=self.headers)
        response.raise_for_status()
        return response
    
    
    def delete_NS(self, device_id: str):
        pass
    
    
    def register_AS(self, device_id: str, dev_eui: str, join_eui: str):
        data = {
            "end_device": {
                "ids": {
                "device_id": device_id,
                "dev_eui": dev_eui,
                "join_eui": join_eui
                }
            },
            "field_mask": {
                "paths": ["ids.device_id", "ids.dev_eui", "ids.join_eui"]
            }
        }
        url = f"{self.base_url}as/applications/{self.app_id}/devices/{device_id}"
        response = requests.put(url, data=json.dumps(data), headers=self.headers)
        response.raise_for_status()
        return response
    
    def delete_AS(self, device_id: str):
        pass