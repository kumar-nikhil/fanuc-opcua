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

## Implementation Approach
When implementing an `asyncua` based client for Fanuc:

1. **Connection URL**: Use `opc.tcp://<ROBOT_IP>:4880/FANUC/NanoUaServer`. (On RoboGuide, it's `127.0.0.1:4880`).
2. **Library**: Use python's `asyncua` standard library.
3. **Data Polling vs Subscriptions**: Fanuc supports MonitoredItems (Publish/Subscribe) with a minimum sampling interval of 100ms. For array elements from the Modbus namespace, partial `DataAccess` (DA) reading via `IndexRange` is preferred.
4. **Data Wrapping**: Expose a clear, object-oriented API in Python so users don't have to concern themselves with string namespace identifiers and just call methods like `.get_alarms()`, `.read_register(1)`.
