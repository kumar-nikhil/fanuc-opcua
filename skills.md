---
name: fanuc-opcua
description: How to read and write data to Fanuc robots using their built-in OPC UA server with the Python asyncua library.
---

# Fanuc OPC UA Node Structure and Interaction

The Fanuc robot controller exposes its data over OPC UA using the standard `NanoUaServer`. There are two main ways the controller models its data via OPC UA:

## 1. Native / System Variables (Namespace 2)
The robot actively provides operational state, alarms, and positions under `ns=2`. These can be browsed and accessed by `NodeId` strings.

**Common `ns=2` Nodes:**
- `ns=2;s=Alarm` : String array of active alarms.
- `ns=2;s=Model` : Robot model (e.g. R-2000iC).
- `ns=2;s=SerialNumber` : Serial number.
- `ns=2;s=Version` : Software revision.
- `ns=2;s=ServoState` : 1/0 indicating if servos are on.
- `ns=2;s=OperationState` : Bitwise integer state (64 = fault, 256 = busy).
- `ns=2;s=ModeState` : Playback mode.
- `ns=2;s=ProgramSpeed` : Speed override percent.
- `ns=2;s=Uptime` : System uptime.
- `ns=2;s=Position` : Position tracking.
- `ns=2;s=Torque` : Axis torque tracking.

## 2. Modbus Target Model (Namespace 1)
According to the official Fanuc **HMI DEVICE COMMUNICATION** guide, the standard Modbus tables are mapped directly into OPC UA at the path `Root/Objects/Modbus`. This is highly useful for reading discrete signals (I/O) and registers. 

By default, they exist in `ns=1`. Since they are mapped as array types, you shouldn't use absolute NodeIDs for each individual bit. Instead, you read from the array at `ns=1;i=301` through `304` using the corresponding Modbus index (`Modbus Address - 1`).

**OPC UA Nodes for Modbus Arrays:**
- `ns=1;i=301` : **DiscreteInput** (Read Only). Maps to Digital Inputs (DI), Robot Inputs (RI), UOP In.
- `ns=1;i=302` : **Coils** (Read/Write). Maps to Digital Outputs (DO), Robot Outputs (RO), Flags.
- `ns=1;i=303` : **InputRegisters** (Read Only). Maps to Group In (GI), Analog In (AI).
- `ns=1;i=304` : **HoldingRegisters** (Read/Write). Maps to assigned robot data including `R[]` (Registers) and `PR[]` (Position Registers).

*Note: Since these Modbus structures are large arrays, it is heavily recommended to use partial reads using the `IndexRange` argument in `asyncua` to avoid performance bottlenecks.*

---

## Developer Usage Guide

Instead of manually navigating the trees with hardcoded OPC commands, the `fanuc-opcua` wrapper handles mapping automatically. When maintaining or extending our codebase, utilize the abstraction API directly rather than the raw library:

### Interacting via Python

**Initialization:**
```python
from fanuc_opcua import FanucClient
client = FanucClient("ip.address.here")
```

**Namespace 2 Handling (Robot Info):**
The `robot_info` module dynamically reads explicit nodes.
```python
alarms_list = await client.robot_info.get_active_alarms()
uptime_string = await client.robot_info.get_uptime()
```

**Namespace 1 Handling (Discrete Logic):**
The `io` module pulls full blocks of Modbus arrays and slices appropriately for one-indexed arrays matching the FANUC UI indices.
```python
is_do_5_on = await client.io.get_digital_output(5) # Returns boolean for DO[5]
```

### Implementing Future Slicing logic
If we must implement HoldingRegisters in the future (`PR` and `R`), the method involves translating Fanuc's `$SNPX_ASG` setup definitions back into python `HoldingRegisters[ns=1;i=304]` index ranges! Be careful with Real vs Signed Int casts across those address offsets.
