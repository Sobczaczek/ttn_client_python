"""
TTN_client - A Python client for interacting with The Things Network API.

MIT License

Copyright (c) 2024 Dawid Sobczak

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import requests
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', handlers=[logging.StreamHandler()]) 

class TTN_client:
    
    class NETWORK_CLUSTER:
        EU1 = "eu1"
        NAM1 = "nam1"
        AU1 = "au1"
        ALL = (EU1, NAM1, AU1)

    class VERSION:
        V3 = "v3"
        ALL = (V3)

    def __init__(self, network_cluster: str, ttn_version: str, app_id: str, api_key: str, app_key: str):
        """Init new class instance object.

        Args:
            network_cluster (str): can be passed as string or TTN_Client.NETWORK_CLUSTER.<()>
            ttn_version (str): can be passed as string or TTN_Client.VERSION.<()>
            app_id (str): unique application identifier
            api_key (str): api key for access
            app_key (str): ...

        Raises:
            ValueError: if network_cluster string is incorect
            ValueError: if version string is incorect
        """
        # validate network cluster
        if network_cluster not in self.NETWORK_CLUSTER.ALL:
            raise ValueError(f"Invalid network cluster: {network_cluster}. Options: {', '.join(self.NETWORK_CLUSTER.ALL)}.")
        self.network_cluster = f"{network_cluster}.cloud.thethings.network"
        
        # validate TTN Version
        if ttn_version not in self.VERSION.ALL:
            raise ValueError(f"Invalid version: {ttn_version}. Options: {', '.join(self.VERSION.ALL)}.")
        self.version = ttn_version

        # assign other attributes
        self.app_key = app_key
        self.app_id = app_id
        self.api_key = api_key
        self.base_url = f"https://{self.network_cluster}/api/{self.version}/"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        
    def info(self):
        """Get all attributes of obejct.

        Returns:
            self: Return all object attributes
        """
        return vars(self)
    
    
    def devices(self) -> requests.Response.json:
        """GET end-device list registered on Identity Server.

        Returns:
            requests.Response.json: list of end-devices, JSON Object
        """
        url = f"{self.base_url}applications/{self.app_id}/devices"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    
    def device(self, device_id: str) -> requests.Response.json:
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
    
        
    def __register_IS(self, device_id: str, dev_eui: str, join_eui: str) -> requests.Response:
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
        # response.raise_for_status()
        return response
    
    
    def __delete_IS(self, device_id: str) -> requests.Response:
        
        url = f"{self.base_url}applications/{self.app_id}/devices/{device_id}"
        response = requests.delete(url, headers=self.headers)
        return response


    def __register_JS(self, device_id: str, dev_eui: str, join_eui: str):
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
        # response.raise_for_status()
        return response
    
    
    def __delete_JS(self, device_id: str):
        
        url = f"{self.base_url}js/applications/{self.app_id}/devices/{device_id}"
        response = requests.delete(url, headers=self.headers)
        return response
    
    
    def __register_NS(self, device_id: str, dev_eui: str, join_eui: str, lorawan_version="1.0.2", lorawan_phy_version="1.0.2-b", frequency_plan_id="EU_863_870_TTN"):
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
        # response.raise_for_status()
        return response
    
    
    def __delete_NS(self, device_id: str):
        url = f"{self.base_url}ns/applications/{self.app_id}/devices/{device_id}"
        response = requests.delete(url, headers=self.headers)
        return response

    
    def __register_AS(self, device_id: str, dev_eui: str, join_eui: str):
        data = {
            "end_device": {
                "ids": {
                    "device_id": device_id,
                    "dev_eui": dev_eui,
                    "join_eui": join_eui
                }
            },
            "field_mask": {
                "paths": [
                    "ids.device_id",
                    "ids.dev_eui",
                    "ids.join_eui"
                ]
            }
        }
        url = f"{self.base_url}as/applications/{self.app_id}/devices/{device_id}"
        response = requests.put(url, data=json.dumps(data), headers=self.headers)
        # response.raise_for_status()
        return response
    
    def __delete_AS(self, device_id: str):
        url = f"{self.base_url}as/applications/{self.app_id}/devices/{device_id}"
        response = requests.delete(url, headers=self.headers)
        return response
    
    
    def __check_response(self, response: requests.Response, step: str):
        
        if response.status_code != 200:
            logging.warning(f"{step} failed. Exiting...")
            return False
        
        return True
    
    
    def __delete_device_sequence(self, device_id: str, delete_steps: list) -> requests.Response:
        """_summary_

        Args:
            device_id (str): _description_
            delete_steps (list): _description_

        Returns:
            requests.Response: _description_
        """
        for delete_step, delete_func in delete_steps:
            logging.info(f"Deleting device on {delete_step}...")
            response = delete_func(device_id)
            
            if not self.__check_response(response, f"Deletion on {delete_step}"):
                return response
            
        logging.info("Deleted all previous steps!")
        return response
    
        
    def otaa(self, device_id: str, dev_eui: str, join_eui: str, 
         lorawan_version="1.0.2", lorawan_phy_version="1.0.2-b", frequency_plan_id="EU_863_870_TTN") -> requests.Response:
        """_summary_

        Args:
            device_id (str): _description_
            dev_eui (str): _description_
            join_eui (str): _description_
            lorawan_version (str, optional): _description_. Defaults to "1.0.2".
            lorawan_phy_version (str, optional): _description_. Defaults to "1.0.2-b".
            frequency_plan_id (str, optional): _description_. Defaults to "EU_863_870_TTN".

        Returns:
            requests.Response: _description_
        """
        
        try:
            logging.info("Create device on the Identity Server")
            response = self.__register_IS(device_id, dev_eui, join_eui)
            if not self.__check_response(response, "Identity Server"):
                return response

            logging.info("Create device on the Join Server")
            response = self.__register_JS(device_id, dev_eui, join_eui)
            if not self.__check_response(response, "Join Server"):
                return self.__delete_device_sequence(device_id, [("Identity Server", self.__delete_IS)])

            logging.info("Create device on the Network Server")
            response = self.__register_NS(device_id, dev_eui, join_eui, lorawan_version, lorawan_phy_version, frequency_plan_id)
            if not self.__check_response(response, "Network Server"):
                return self.__delete_device_sequence(device_id, [("Join Server", self.__delete_JS), ("Identity Server", self.__delete_IS)])

            logging.info("Create device on the Application Server")
            response = self.__register_AS(device_id, dev_eui, join_eui)
            if not self.__check_response(response, "Application Server"):
                return self.__delete_device_sequence(device_id, [("Network Server", self.__delete_NS), ("Join Server", self.__delete_JS), ("Identity Server", self.__delete_IS)])
        
        except Exception as err:
            logging.error(f"Exception occurred: {err}")
            return response if 'response' in locals() else None
        
        else:
            logging.info(f"Device `{device_id}` created successfully!")
            return response

        
    def delete_device(self, device_id: str) -> requests.Response:
        
        delete_steps = [
            ("Application Server", self.__delete_AS),
            ("Network Server", self.__delete_NS), 
            ("Join Server", self.__delete_JS), 
            ("Identity Server", self.__delete_IS)
        ]
        
        return self.__delete_device_sequence(device_id, delete_steps) 
        