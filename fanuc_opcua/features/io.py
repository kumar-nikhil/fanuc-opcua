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
        node = self._client.get_node(ModbusNodes.DISCRETE_INPUT)
        return await node.read_value()

    async def _read_coils_array(self):
        node = self._client.get_node(ModbusNodes.COILS)
        return await node.read_value()

    async def _get_discrete_bit(self, offset: int, index: int) -> bool:
        arr = await self._read_discrete_input_array()
        return bool(arr[(offset - 1) + (index - 1)])

    async def _get_coil_bit(self, offset: int, index: int) -> bool:
        arr = await self._read_coils_array()
        return bool(arr[(offset - 1) + (index - 1)])

    # --- Discrete Inputs (Read Only) ---
    async def get_digital_input(self, index: int) -> bool:
        if index < 1 or index > 10000: raise ValueError("DI index out of bounds")
        return await self._get_discrete_bit(1, index)

    async def get_robot_input(self, index: int) -> bool:
        if index < 1 or index > 10000: raise ValueError("RI index out of bounds")
        return await self._get_discrete_bit(10001, index)

    async def get_uop_input(self, index: int) -> bool:
        if index < 1 or index > 10000: raise ValueError("UI index out of bounds")
        return await self._get_discrete_bit(20001, index)

    async def get_uop_output(self, index: int) -> bool:
        if index < 1 or index > 1000: raise ValueError("UO index out of bounds")
        return await self._get_discrete_bit(21001, index)
    
    async def get_sop_input(self, index: int) -> bool:
        # SOP input maps SI[0-999], we use 1-based index in our python API conventionally or 0 based?
        # PDF says 22000 ~ 22999 SOP input SI[0-999]
        if index < 0 or index > 999: raise ValueError("SI index out of bounds")
        return await self._get_discrete_bit(22000, index + 1)
        
    async def get_sop_output(self, index: int) -> bool:
        # 23000 ~ 24000 SOP output SO[0-1000]
        if index < 0 or index > 1000: raise ValueError("SO index out of bounds")
        return await self._get_discrete_bit(23000, index + 1)

    # --- Coils (Read / Write) ---
    async def get_digital_output(self, index: int) -> bool:
        if index < 1 or index > 10000: raise ValueError("DO index out of bounds")
        return await self._get_coil_bit(1, index)

    async def get_robot_output(self, index: int) -> bool:
        if index < 1 or index > 10000: raise ValueError("RO index out of bounds")
        return await self._get_coil_bit(10001, index)

    async def get_flag(self, index: int) -> bool:
        if index < 1 or index > 10000: raise ValueError("F index out of bounds")
        return await self._get_coil_bit(20001, index)
