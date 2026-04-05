import pytest
import struct
from unittest.mock import AsyncMock, MagicMock
from fanuc_opcua.features.registers import Registers

@pytest.mark.asyncio
async def test_holding_register_unpacking():
    """
    Test that the unpacking logic for holding registers correctly 
    translates raw signed 16-bit word pairs from Modbus into Python primitives.
    """
    client_mock = MagicMock()
    # Mock get_node
    node_mock = AsyncMock()
    client_mock.get_node.return_value = node_mock
    
    # We will simulate an array of Int16 return values.
    # For a REAL type: 123.45 in IEEE 754 is:
    # 0x42F6E666
    # Broken into Little Endian 16-bit words: E666 and 42F6
    # Natively as Signed Ints: 
    # E666 = -6554
    # 42F6 = +17142
    node_mock.read_value.return_value = [-6554, 17142]
    
    registers = Registers(client_mock)
    
    # Test unpacking REAL
    # word0 = -6554, word1 = 17142
    val = await registers.read_holding_register(1, "real")
    
    # Check if value matches floating point precision closely
    assert val is not None
    assert abs(val - 123.45) < 0.001

@pytest.mark.asyncio
async def test_holding_register_int32():
    client_mock = MagicMock()
    node_mock = AsyncMock()
    client_mock.get_node.return_value = node_mock
    
    # For an INT32: 123456789
    # Hex: 0x075BCD15
    # Words: CD15, 075B
    # Natively as Signed Ints:
    # CD15 = -13035
    # 075B = 1883
    
    node_mock.read_value.return_value = [-13035, 1883]
    
    registers = Registers(client_mock)
    
    val = await registers.read_holding_register(1, "int32")
    assert val == 123456789

@pytest.mark.asyncio
async def test_holding_register_int16():
    client_mock = MagicMock()
    node_mock = AsyncMock()
    client_mock.get_node.return_value = node_mock
    
    # Simple INT16: -450
    node_mock.read_value.return_value = [-450, 0]
    
    registers = Registers(client_mock)
    val = await registers.read_holding_register(1, "int16")
    
    assert val == -450
