from asyncua import Client
import logging

from .features.robot_info import RobotInfo
from .features.registers import Registers

logger = logging.getLogger(__name__)

class FanucClient:
    """
    An easy to use Python client for Fanuc Robot OPC UA connections.
    """
    def __init__(self, ip_address: str, port: int = 4880):
        # Format the endpoint as expected by Fanuc NanoUaServer
        self.endpoint = f"opc.tcp://{ip_address}:{port}/FANUC/NanoUaServer"
        self._client = Client(url=self.endpoint)
        
        # Attach feature wrappers
        self.robot_info = RobotInfo(self._client)
        self.registers = Registers(self._client)

    async def connect(self):
        """Connects to the Fanuc OPC UA Server."""
        logger.info(f"Connecting to Fanuc Robot at {self.endpoint}")
        await self._client.connect()
        logger.info("Connection established.")

    async def disconnect(self):
        """Disconnects from the Fanuc OPC UA Server."""
        await self._client.disconnect()
        logger.info("Disconnected from Fanuc Robot.")

    # Context manager support
    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()
