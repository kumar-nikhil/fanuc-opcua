from asyncua import Client
from ..nodes import ModbusNodes

class Registers:
    """
    Handles interacting with Fanuc Modbus mapped arrays (Registers, I/O).
    Currently a placeholder for advanced index/slice implementation.
    """
    def __init__(self, client: Client):
        self._client = client

    # TODO: Implement array indexing via NumericRange or full array retrieval
    # depending on what is most optimal for typical scenarios.
