# This code is based on the Sagemcom API documentation available at:
# https://github.com/iMicknl/python-sagemcom-api

import asyncio
from sagemcom_api.client import SagemcomClient
from sagemcom_api.enums import EncryptionMethod
from sagemcom_api.exceptions import NonWritableParameterException



HOST = "192.168.1.1" #default address
USERNAME = "USERNAME"
PASSWORD = "PASSWORD"
ENCRYPTION_METHOD = EncryptionMethod.MD5 

async def get_devices() -> None:
    async with SagemcomClient(HOST, USERNAME, PASSWORD, ENCRYPTION_METHOD) as client:
        try:
            await client.login()
        except Exception as exception: 
            return exception

        messages=[]

        # Get connected devices
        devices = await client.get_hosts()

        for device in devices:
            if device.active:
                if not device.name:
                    device_name = "Unknown"
                else:
                    device_name = device.name 
                
                message = (f"*Name:* `{device_name}`\n"
                       f"\tMac: `{device.id}`\n"
                       f"\tIP: `{device.ip_address}`\n"
                       f"\tType: _{device.interface_type}_\n")
                messages.append(message)
        return messages

#asyncio.run(get_devices())