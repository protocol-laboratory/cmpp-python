import asyncio

from cmpp.constants import CONNECT_ID
from cmpp.protocol import CmppConnect, CmppPdu, CmppHeader
from cmpp.utils import BoundAtomic


class CmppClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.sequence_id = BoundAtomic(1, 0x7FFFFFFF)
        self.reader = None
        self.writer = None

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)

    async def connect_ismg(self, request: CmppConnect):
        if self.writer is None or self.reader is None:
            raise ConnectionError("Client is not connected")
        sequence_id = self.sequence_id.next_val()
        header = CmppHeader(0, command_id=CONNECT_ID, sequence_id=sequence_id)
        pdu: CmppPdu = CmppPdu(header=header, body=request)
        self.writer.write(pdu.encode())
        await self.writer.drain()

        length_bytes = await self.reader.readexactly(4)
        response_length = int.from_bytes(length_bytes)

        response_data = await self.reader.readexactly(response_length)

        return CmppPdu.decode(response_data)

    async def close(self):
        if self.writer:
            self.writer.close()
