from asyncua import Client
from ..nodes import NodeKeys

class RobotInfo:
    """
    Handles reading native Fanuc system state nodes (ns=2).
    """
    def __init__(self, client: Client):
        self._client = client

    async def _read_node(self, node_id: str):
        node = self._client.get_node(node_id)
        return await node.read_value()

    async def get_model(self) -> str:
        """Returns the Robot model name."""
        return await self._read_node(NodeKeys.MODEL)

    async def get_serial_number(self) -> str:
        """Returns the Robot serial number."""
        return await self._read_node(NodeKeys.SERIAL_NUMBER)

    async def get_version(self) -> str:
        """Returns the software version."""
        return await self._read_node(NodeKeys.VERSION)

    async def get_active_alarms(self) -> list:
        """Returns a list of currently active alarms. Filters out empty strings."""
        alarms = await self._read_node(NodeKeys.ALARM)
        if isinstance(alarms, list):
            return [str(a) for a in alarms if a and str(a).strip()]
        elif alarms:
            return [str(alarms)]
        return []

    async def get_servo_state(self) -> bool:
        """Returns True if Servos are ON, False otherwise."""
        state = await self._read_node(NodeKeys.SERVO_STATE)
        return bool(state)
        
    async def get_operation_state(self) -> int:
        """Returns the bitwise integer of the current operational state."""
        return await self._read_node(NodeKeys.OPERATION_STATE)

    async def get_mode_state(self) -> int:
        """Returns the mode state (e.g. AUTO, T1, T2)."""
        return await self._read_node(NodeKeys.MODE_STATE)

    async def get_program_speed(self) -> int:
        """Returns the program speed override percentage."""
        return await self._read_node(NodeKeys.PROGRAM_SPEED)
        
    async def get_uptime(self) -> str:
        """Returns the system uptime."""
        val = await self._read_node(NodeKeys.UPTIME)
        return str(val)

    async def get_position(self):
        """Returns the current position (representation format may vary)."""
        return await self._read_node(NodeKeys.POSITION)

    async def get_torque(self):
        """Returns the current axis torque."""
        return await self._read_node(NodeKeys.TORQUE)
