import asyncio
from cmpp.client import CmppClient
from cmpp.protocol import CmppConnect


async def main():
    client = CmppClient(host='localhost', port=7890)

    await client.connect()
    print("Connected to ISMG")

    connect_request = CmppConnect(
        source_addr='source_addr',
        authenticator_source=b'authenticator_source',
        version=0,
        timestamp=1122334455,
    )

    connect_response = await client.connect_ismg(connect_request)
    print(f"Connect response: {connect_response}")

    await client.close()
    print("Connection closed")


asyncio.run(main())
