# ttn_client

**TTN_client** - A Python client for interacting with The Things Network API.

## Overview

`ttn_client` is a Python library that allows you to interact with The Things Network (TTN) API. It simplifies the process of managing devices, applications, and communication with the TTN backend.

## Features

- **Device Management**: Register, delete, and manage devices on the Identity Server (IS), Join Server (JS), Network Server (NS), and Application Server (AS).
- **Device Information Retrieval**: Retrieve details about registered devices.
- **Over-the-Air Activation (OTAA)**: Perform OTAA operations to provision devices on the network.

## Installation

You can install the package using `pip`:

```bash
pip install ttn_client
```

## Usage

Here's a quick example of how to use the `ttn_client` package:

```python
from ttn_client import TTN_client

# Initialize the client
client = TTN_client(
    network_cluster=TTN_client.NETWORK_CLUSTER.EU1,
    ttn_version=TTN_client.VERSION.V3,
    app_id='your_app_id',
    api_key='your_api_key',
    app_key='your_app_key'
)

# Get information about the client
print(client.info())

# List devices
devices = client.get_devices()
print(devices)

# Get information about a specific device
device_info = client.get_device('device_id')
print(device_info)

# Register a device using OTAA
response = client.otaa(
    device_id='new_device_id',
    dev_eui='your_dev_eui',
    join_eui='your_join_eui',
    lorawan_version="1.0.2",
    lorawan_phy_version="1.0.2-b",
    frequency_plan_id="EU_863_870_TTN"
)
print(response)

# Delete a device
delete_response = client.delete_end_device('device_id')
print(delete_response)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## Author

**Dawid Sobczak**  
Email: [sobczakss111@gmail.com](mailto:sobczakss111@gmail.com)

## Acknowledgements

This package was inspired by the need for a simple and effective way to interact with The Things Network API using Python.
