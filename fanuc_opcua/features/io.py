from asyncua import Client
from ..nodes import ModbusNodes
import logging

logger = logging.getLogger(__name__)

class IO:
    """
    Handles reading and writing discrete I/O from the Modbus NameSpace (ns=1).
    """
    def __init__(self, client: Client):
        self._client = client

    async def _read_discrete_input_array(self):
        """Reads the entire DiscreteInput array."""
        node = self._client.get_node(ModbusNodes.DISCRETE_INPUT)
        return await node.read_value()

    async def _read_coils_array(self):
        """Reads the entire Coils array."""
        node = self._client.get_node(ModbusNodes.COILS)
        return await node.read_value()

    async def get_digital_input(self, index: int) -> bool:
        """
        Reads a Digital Input (DI).
        Index parameter is 1-based (DI[1] -> index 1)
        """
        if index < 1 or index > 10000:
            raise ValueError("DI index must be between 1 and 10000.")
        
        # Modbus address for DI is 1~10000, 0-based array index is index - 1
        arr = await self._read_discrete_input_array()
        return bool(arr[index - 1])

    async def get_digital_output(self, index: int) -> bool:
        """
        Reads a Digital Output (DO).
        Index parameter is 1-based (DO[1] -> index 1)
        """
        if index < 1 or index > 10000:
            raise ValueError("DO index must be between 1 and 10000.")
        
        # Modbus address for DO is 1~10000, 0-based array index is index - 1
        arr = await self._read_coils_array()
        return bool(arr[index - 1])

    # Note: Setting individual bits in an OPC UA array can be tricky if
    # the server doesn't support 'IndexRange' writes natively. We will 
    # need to explore robust index_range writes or write the entire array back out.
    async def set_digital_output(self, index: int, value: bool):
        """
        Sets a Digital Output (DO).
        Index parameter is 1-based (DO[1] -> index 1)
        """
        logger.warning("Writing to Coils currently unimplemented while evaluating 'IndexRange' support for NanoUaServer.")
        pass
