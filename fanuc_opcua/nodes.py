"""
Mappings for Fanuc OPC UA Nodes
"""

class Namespaces:
    MODBUS = 1
    FANUC = 2

class NodeKeys:
    """
    Standard NS=2 Nodes exposed by Fanuc.
    """
    ALARM = "ns=2;s=Alarm"
    MODEL = "ns=2;s=Model"
    SERIAL_NUMBER = "ns=2;s=SerialNumber"
    VERSION = "ns=2;s=Version"
    SERVO_STATE = "ns=2;s=ServoState"
    OPERATION_STATE = "ns=2;s=OperationState"
    MODE_STATE = "ns=2;s=ModeState"
    PROGRAM_SPEED = "ns=2;s=ProgramSpeed"
    UPTIME = "ns=2;s=Uptime"
    POSITION = "ns=2;s=Position"
    TORQUE = "ns=2;s=Torque"

class ModbusNodes:
    """
    Standard NS=1 Modbus mappings (Array Access)
    Actual Index is (Modbus Address - 1)
    """
    DISCRETE_INPUT = "ns=1;i=301"     # Read Only: DI, RI, UI
    COILS = "ns=1;i=302"              # Read/Write: DO, RO, F
    INPUT_REGISTERS = "ns=1;i=303"    # Read Only: GI, AI
    HOLDING_REGISTERS = "ns=1;i=304"  # Read/Write: R, PR, GO, AO
