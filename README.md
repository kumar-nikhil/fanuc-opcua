# fanuc-opcua

An easy-to-use, pythonic OPC UA client library for communicating with Fanuc Robot controllers.

## Overview
Fanuc robots that have the OPC UA server option enabled expose various information arrays including Registers, Strings, Current Position, and Operational Status. 

Usually, reading this data entails writing low-level scripts managing NodeIDs and namespaces. `fanuc-opcua` abstracts the Fanuc `NanoUaServer` complexity using `asyncua` and provides a clean asynchronous API for typical data read/write workflows.

## Installation

```bash
pip install fanuc-opcua
```

## Quick Start

The library uses the standard python `asyncio` framework. Connection string targets the Fanuc controller IP.

```python
import asyncio
from fanuc_opcua import FanucClient

async def main():
    # Use context manager for auto connect/disconnect
    async with FanucClient("192.168.1.100") as robot:
        
        # 1. System Information
        model = await robot.robot_info.get_model()
        print(f"Connected to {model} robot!")
        
        version = await robot.robot_info.get_version()
        print(f"Software Version: {version}")

        # 2. Operational State
        alarms = await robot.robot_info.get_active_alarms()
        print(f"Active Alarms: {alarms}") # Cleanly filtered list
        
        mode = await robot.robot_info.get_mode_state()
        print(f"Mode: {mode}")

        # 3. Position and Motion
        position_data = await robot.robot_info.get_position()
        print(f"Position (X, Y, Z, W, P, R): {position_data}")

        # 4. Discrete Modbus I/O (DI/DO mapped natively)
        # Check Digital Input [1] -> D[1]
        is_active = await robot.io.get_digital_input(1) 
        print(f"DI[1] active: {is_active}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Available API Namespaces

### `FanucClient.robot_info`
Access to device-level Namespace 2 nodes:
- `.get_model()` -> `str`
- `.get_serial_number()` -> `str`
- `.get_version()` -> `str`
- `.get_active_alarms()` -> `list[str]`
- `.get_servo_state()` -> `bool`
- `.get_operation_state()` -> `int`
- `.get_mode_state()` -> `int`
- `.get_program_speed()` -> `int` 
- `.get_uptime()` -> `str`
- `.get_position()` -> `list[float]`
- `.get_torque()` -> `list[float]`

### `FanucClient.io`
Access to the discrete I/O structures (Namespace 1 Modbus mappings):
- `.get_digital_input(index)` -> `bool`
- `.get_digital_output(index)` -> `bool`

*(Note: Index numbers map strictly to Fanuc controller syntax, e.g. `index 1` resolves to `DI[1]`.)*
