# Author: João S. O. Bueno
# License: LGPL v.3.0+

import struct
import random
import enum


class Status(enum.Enum):
    created = 0
    sent = 1
    answered = 2


sent_messages = dict()
response_registry = {}


def instantiate(payload):
    message_type = Message.get_message_type(payload)
    cls = response_registry[message_type]
    message = cls()
    message.extract(payload)
    return message


class MessageStatus:
    __slots__ = ("source", "response", "status")

    def __init__(self, status=None, source=None, response=None):
        self.status = status
        self.source  = source
        self.response = response


class Message:
    rsvd = 0
    ver = 1
    message_type = 0
    message_id = 0

    def __init__(self):
        self.message_id = random.randrange(0, 2**32)
        sent_messages[self.message_id] = MessageStatus(Status.created, self)

    def pack_message_type(self):
        value = self.rsvd << 13 |self.ver << 10 | self.message_type
        return value

    @property
    def message_length(self):
        return 16 + 32 + 32

    def render(self):
        return struct.pack("HII", self.pack_message_type(), self.message_length, self.message_id)

    def _split_payload(self, struct_info, payload)
        size = struct.calcsize(struct_info)
        return payload[:size], payload[size:]

    @staticmethod
    def get_message_type(payload):
        message_type_pack, = struct.unpack("H", payload[:2])
        return message_type_pack & (2 ** 10 - 1)


    def extract(self, payload):
        payload, remainder = self._split_payload("HII", payload)
        message_type_pack, message_length, message_id = struct.unpack("HII", payload)
        if message_length != len(payload):
            raise ValueError("Incorrect message length real: {}, indicated: {}".format(
                len(payload), message_length))
        message_type = message_type_pack & (2 ** 10 - 1)
        if message_type != self.message_type:
            # TODO: implement a factory to instantiate the apropriate
            # "ReaderMessage" subclass from the message type
            raise ValueError("Incompatible message type")

        self.ver = (message_type_pack >> 10) & 0b111
        return remainder


    def __repr__(self):
        return "<{}, ({}) type: {}>".format(
            self.__class__.__name__,
            "client" if isinstance(self, ClientMessage) else "reponse",
            self.message_type)


class ClientMessage(Message):
    pass


class ReaderMessage(Message):
    pass



class GetSupportedVersion(ClientMessage):
    message_type = 46


class GetSupportedVersionResponse(ReaderMessage):
    message_type = 56
    def extract(self, payload):
        payload = super().extract(payload)
        payload, remainder = selr._split_payload("HH", payload)
        self.current_version, self.supported_version = struct.unpack("HH", payload)
        return remainder

response_registry[GetSupportedVersionResponse.message_type] = GetSupportedVersionResponse


