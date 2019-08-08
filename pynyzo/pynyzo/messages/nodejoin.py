import json
import struct

from pynyzo.messageobject import MessageObject

from pynyzo.fieldbytesize import FieldByteSize
from pynyzo.helpers import base_app_log
from pynyzo.messagetype import MessageType


class NodeJoin(MessageObject):
    """NodeJoin message"""

    __slots__ = ('_port_tcp', '_nickname')

    def __init__(self, port_tcp: int, nickname: str, app_log=None):
        super().__init__(app_log=app_log)
        self._port_tcp = port_tcp
        self._nickname = nickname

    def get_byte_size(self) -> int:
        return FieldByteSize.port + FieldByteSize.string(self._nickname) if self._nickname is not None \
            else FieldByteSize.string('')

    def get_bytes(self) -> bytes:
        result = []
        result.append(struct.pack(">I", self._port_tcp))
        # add nickname length and nickname to the bytes buffer if nickname is not none, otherwise add only short with
        # length of the nickname 0
        if self._nickname is not None:
            result.append(struct.pack(">h", len(self._nickname)))
            result.append(self._nickname.encode())
        else:
            result.append(struct.pack(">h", 0))
        return b''.join(result)

    def to_string(self) -> str:
        return f"[NodeJoin({self._port_tcp}, {self._nickname})]"

    def to_json(self) -> str:
        return json.dumps({"message_type": MessageType.NodeJoin3.name, 'value': {
            'port_tcp': self._port_tcp, 'nickname': self._nickname}})

    def print(self):
        """Create the status message and print it"""
        app_log = base_app_log()
        app_log.info(self.to_string())
