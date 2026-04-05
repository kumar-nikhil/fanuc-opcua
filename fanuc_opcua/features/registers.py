import struct
from asyncua import Client
from ..nodes import ModbusNodes
import logging

logger = logging.getLogger(__name__)

class Registers:
    """
    Handles interacting with Fanuc Modbus mapped arrays (Registers, I/O).
    """
    def __init__(self, client: Client):
        self._client = client

    # --- Input Registers (ns=1;i=303) ---
    async def _read_input_registers_array(self):
        node = self._client.get_node(ModbusNodes.INPUT_REGISTERS)
        return await node.read_value()

    async def _get_input_register(self, offset: int, index: int) -> int:
        arr = await self._read_input_registers_array()
        return arr[(offset - 1) + (index - 1)]

    async def get_group_input(self, index: int) -> int:
        if index < 1 or index > 1000: raise ValueError("GI index out of bounds")
        return await self._get_input_register(1, index)

    async def get_group_output(self, index: int) -> int:
        if index < 1 or index > 1000: raise ValueError("GO index out of bounds")
        return await self._get_input_register(1001, index)

    async def get_analog_input(self, index: int) -> int:
        if index < 1 or index > 1000: raise ValueError("AI index out of bounds")
        return await self._get_input_register(2001, index)

    async def get_analog_output(self, index: int) -> int:
        if index < 1 or index > 1000: raise ValueError("AO index out of bounds")
        return await self._get_input_register(3001, index)

    # --- Holding Registers (ns=1;i=304) ---
    async def _read_holding_registers_array(self):
        node = self._client.get_node(ModbusNodes.HOLDING_REGISTERS)
        return await node.read_value()

    async def read_holding_register(self, address: int, data_type: str = "int16"):
        """
        Generic method to read mapped HoldingRegisters (e.g. R[], PR[], SR[]).
        Address is 1-based (matches Modbus standard address).
        Supported data_type: "int16", "int32", "real"
        """
        if address < 1 or address > 16384: raise ValueError("Holding register address out of bounds")
        
        arr = await self._read_holding_registers_array()
        
        # Address 1 = index 0
        idx = address - 1
        
        if data_type.lower() == "int16":
            return arr[idx]
            
        elif data_type.lower() in ["int32", "real"]:
            # Fanuc uses 2 holding registers for 32-bit values.
            # "The former address is lower 16 bits data, and the latter address is upper 16bits data."
            word0 = arr[idx]      # Low 16 bits (signed int16 natively in UA)
            word1 = arr[idx + 1]  # High 16 bits (signed int16)
            
            # Pack two SIGNED 16-bit ints natively, forcing standard little-endian placement 
            # to reconstruct the 32-bit sequence properly. 
            # Python struct: 'h' is native short (2 bytes), '<hh' packs it as little-endian words.
            try:
                b = struct.pack('<hh', word0, word1)
                
                if data_type.lower() == "int32":
                    return struct.unpack('<i', b)[0]
                elif data_type.lower() == "real":
                    return struct.unpack('<f', b)[0]
            except Exception as e:
                logger.error(f"Failed to unpack 32-bit data format from Holding Registers: {e}")
                return None
                
        else:
            raise ValueError(f"Unsupported data_type: {data_type}")
