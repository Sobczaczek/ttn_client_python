import requests
import json
import logging

logging.basicConfig(level=logging.INFO,  # Set the logging level
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Set the logging format
                    handlers=[logging.StreamHandler()]) 

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
        
        url = f"{self.base_url}js/applications/{self.app_id}/devices/{device_id}"
        response = requests.delete(url, headers=self.headers)
        return response
    
    
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

        url = f"{self.base_url}ns/applications/{self.app_id}/devices/{device_id}"
        response = requests.delete(url, headers=self.headers)
        return response

    
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

        url = f"{self.base_url}as/applications/{self.app_id}/devices/{device_id}"
        response = requests.delete(url, headers=self.headers)
        return response
    
    
    # def otaa(self, device_id: str, dev_eui: str, join_eui: str, 
    #          lorawan_version="1.0.2", lorawan_phy_version="1.0.2-b", frequency_plan_id="EU_863_870_TTN") -> requests.Response:
        
    #     try:
    #         # create device on IS
    #         logging.info("Create device on the Identity Server")
    #         response = self.register_IS(device_id, dev_eui, join_eui)
            
    #         # check for valid HTTP_200
    #         if not response.status_code == 200:
    #             logging.warning("Identity Server failed. Exiting...")
    #             return response
            
    #         # create device on JS
    #         logging.info("Create device on the Join Server")
    #         response = self.register_JS(device_id, dev_eui, join_eui)
                        
    #         # check for valid HTTP_200
    #         if not response.status_code == 200:
                
    #             # delete device on IS
    #             logging.warning("Join Server failed. Deleting device on Identity Server...")
    #             response = self.delete_IS(device_id)
                
    #             # check for valid HTTP_200
    #             if not response.status_code == 200:
    #                 logging.warning("Deletion failed. Exiting...")
    #                 return response
                
    #             # return response for failed JS 
    #             logging.info("Deleted!")
    #             return response
            
    #         # create device on NS
    #         logging.info("Create device on the Network Server")
    #         response = self.register_NS(device_id, dev_eui, join_eui, lorawan_version, lorawan_phy_version, frequency_plan_id)

    #         # check valid HTTP_200
    #         if not response.status_code == 200:
                
    #             # delete device on JS
    #             logging.warning("Network Server failed. Deleting device on Join Server...")
    #             response = self.delete_JS(device_id)
                
    #             # check for valid HTTP_200
    #             if not response.status_code == 200:
    #                 logging.warning("Deletion failed. Exiting...")
    #                 return response

    #             # delete device on ID
    #             logging.info("Deleted. Deleting device on Identity Server...")
    #             response = self.delete_IS(device_id)

    #             # check for valid HTTP_200
    #             if not response.status_code == 200:
    #                 logging.warning("Deletion failed. Exiting...")
    #                 return response

    #             # return response for failed NS
    #             logging.info("Deleted!")
    #             return response
            
    #         # create device on AS
    #         logging.info("Create device on the Application Server")
    #         response = self.register_AS(device_id, dev_eui, join_eui)

    #         # check valid HTTP_200
    #         if not response.status_code == 200:

    #             # delete device on AS
    #             logging.warning("Application Server failed. Deleting device on Network Server...")
    #             response = self.delete_AS(device_id)
                
    #             # check for valid HTTP_200
    #             if not response.status_code == 200:
    #                 logging.warning("Deletion failed. Exiting...")
    #                 return response

    #             # delete device on JS
    #             logging.info("Deleted. Deleting device on Join Server...")
    #             response = self.delete_JS(device_id)

    #             # check for valid HTTP_200
    #             if not response.status_code == 200:
    #                 logging.warning("Deletion failed. Exiting...")
    #                 return response
                
    #             # delete device on IS
    #             logging.info("Deleted. Deleting device on Identity Server...")
    #             response = self.delete_IS(device_id)

    #             # check for valid HTTP_200
    #             if not response.status_code == 200:
    #                 logging.warning("Deletion failed. Exiting...")
    #                 return response

    #             # return response for failed AS
    #             logging.info("Deleted!")
    #             return response
            
    #         logging.info(f"Device `{device_id}` created!")
    #         return response
        
    #     except Exception as err:
    #         logging.error(err)
    #         return response      
    
    def otaa(self, device_id: str, dev_eui: str, join_eui: str, 
         lorawan_version="1.0.2", lorawan_phy_version="1.0.2-b", frequency_plan_id="EU_863_870_TTN") -> requests.Response:
    
        def check_response(response: requests.Response, step: str):
            if response.status_code != 200:
                logging.warning(f"{step} failed. Exiting...")
                return False
            return True

        def delete_device_sequence(device_id: str, delete_steps: list):
            for delete_step, delete_func in delete_steps:
                logging.info(f"Deleting device on {delete_step}...")
                response = delete_func(device_id)
                if not check_response(response, f"Deletion on {delete_step}"):
                    return response
            logging.info("Deleted all previous steps!")
            return response
        
        try:
            logging.info("Create device on the Identity Server")
            response = self.register_IS(device_id, dev_eui, join_eui)
            if not check_response(response, "Identity Server"):
                return response

            logging.info("Create device on the Join Server")
            response = self.register_JS(device_id, dev_eui, join_eui)
            if not check_response(response, "Join Server"):
                return delete_device_sequence(device_id, [("Identity Server", self.delete_IS)])

            logging.info("Create device on the Network Server")
            response = self.register_NS(device_id, dev_eui, join_eui, lorawan_version, lorawan_phy_version, frequency_plan_id)
            if not check_response(response, "Network Server"):
                return delete_device_sequence(device_id, [("Network Server", self.delete_NS), ("Join Server", self.delete_JS), ("Identity Server", self.delete_IS)])

            logging.info("Create device on the Application Server")
            response = self.register_AS(device_id, dev_eui, join_eui)
            if not check_response(response, "Application Server"):
                return delete_device_sequence(device_id, [("Application Server", self.delete_AS), ("Network Server", self.delete_NS), ("Join Server", self.delete_JS), ("Identity Server", self.delete_IS)])

            logging.info(f"Device `{device_id}` created successfully!")
            return response
        
        except Exception as err:
            logging.error(f"Exception occurred: {err}")
            return response if 'response' in locals() else None

        
         