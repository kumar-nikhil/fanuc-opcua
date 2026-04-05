import asyncio
from fanuc_opcua import FanucClient

async def main():
    print("Testing connection to Fanuc RoboGuide OPC UA Server at localhost:4880...")
    
    # Use context manager for auto connect/disconnect
    async with FanucClient("127.0.0.1") as robot:
        try:
            model = await robot.robot_info.get_model()
            print(f"[SUCCESS] Connected to robot model: {model}")
            
            uptime = await robot.robot_info.get_uptime()
            print(f"[INFO] Uptime: {uptime}")
            
            alarms = await robot.robot_info.get_active_alarms()
            print(f"[INFO] Active Alarms: {alarms}")
            
        except Exception as e:
            print(f"[ERROR] Failed to communicate: {e}")

if __name__ == "__main__":
    asyncio.run(main())
