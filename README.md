# fanuc-opcua

An easy-to-use, pythonic OPC UA client library for communicating with Fanuc Robot controllers.

## Overview
Fanuc robots that have the OPC UA server option enabled expose various information arrays including Registers, Strings, Current Position, and Operational Status. 

Usually, reading this data entails writing low-level scripts managing NodeIDs and namespaces. `fanuc-opcua` abstracts the Fanuc `NanoUaServer` complexity using `asyncua` and provides a clean asynchronous API for typical data read/write workflows.

## Installation

```bash
pip install -e .
```

## Setup & Demo Let's get started.

```python
import asyncio
from fanuc_opcua import FanucClient

async def main():
    # Substitute localhost with your Robot IP or RoboGuide PC IP
    client = FanucClient("127.0.0.1")
    
    async with client:
        model = await client.robot_info.get_model()
        print(f"Connected to {model} robot!")
        
        # Access alarms
        alarms = await client.robot_info.get_active_alarms()
        print("Active Alarms:", alarms)

if __name__ == "__main__":
    asyncio.run(main())
```
