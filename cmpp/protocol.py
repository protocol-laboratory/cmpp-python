from dataclasses import dataclass
from typing import Union, List

from cmpp.constants import CONNECT_RESP_ID


@dataclass
class CmppHeader:
    total_length: int
    command_id: int
    sequence_id: int


@dataclass
class CmppConnect:
    source_addr: str
    authenticator_source: bytes
    version: int
    # MMDDHHMMSS format
    timestamp: int

    def encode(self) -> bytes:
        source_addr_bytes = self.source_addr.encode('utf-8').ljust(6, b'\x00')
        version_byte = self.version.to_bytes(1, 'big')
        timestamp_bytes = self.timestamp.to_bytes(4, 'big')
        return source_addr_bytes + self.authenticator_source + version_byte + timestamp_bytes


@dataclass
class CmppConnectResp:
    status: int
    authenticator_ismg: str
    version: int

    @staticmethod
    def decode(data: bytes) -> 'CmppConnectResp':
        status = int.from_bytes(data[0:4], 'big')
        authenticator_ismg = data[4:20].rstrip(b'\x00').decode('utf-8')
        version = data[20]
        return CmppConnectResp(status=status, authenticator_ismg=authenticator_ismg, version=version)


@dataclass
class CmppSubmit:
    msg_id: int
    pk_total: int
    pk_number: int
    registered_delivery: int
    msg_level: int
    service_id: str
    fee_user_type: int
    fee_terminal_id: str
    fee_terminal_type: int
    tp_pid: int
    tp_udhi: int
    msg_fmt: int
    msg_src: str
    fee_type: str
    fee_code: str
    valid_time: str
    at_time: str
    src_id: str
    dest_usr_tl: int
    dest_terminal_id: List[str]
    dest_terminal_type: int
    msg_length: int
    msg_content: bytes
    link_id: str


@dataclass
class CmppSubmitResp:
    msg_id: int
    result: int


@dataclass
class CmppPdu:
    header: CmppHeader
    body: Union[CmppConnect, CmppConnectResp, CmppSubmit, CmppSubmitResp]

    def encode(self) -> bytes:
        body_bytes = self.body.encode()
        self.header.total_length = len(body_bytes) + 12
        header_bytes = (self.header.total_length.to_bytes(4, 'big') +
                        self.header.command_id.to_bytes(4, 'big') +
                        self.header.sequence_id.to_bytes(4, 'big'))
        return header_bytes + body_bytes

    @staticmethod
    def decode(data: bytes) -> 'CmppPdu':
        header = CmppHeader(total_length=int.from_bytes(data[0:4], 'big'),
                            command_id=int.from_bytes(data[4:8], 'big'),
                            sequence_id=int.from_bytes(data[8:12], 'big'))

        body_data = data[12:header.total_length]
        if header.command_id == CONNECT_RESP_ID:
            body = CmppConnectResp.decode(body_data)
        else:
            raise NotImplementedError("not implemented yet.")

        return CmppPdu(header=header, body=body)
