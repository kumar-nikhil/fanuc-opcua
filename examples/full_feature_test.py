import asyncio
from fanuc_opcua import FanucClient

async def main():
    print("=== Testing all Fanuc OPC UA Features ===")
    
    async with FanucClient("127.0.0.1") as robot:
        print("\n--- 1. System Information ---")
        model = await robot.robot_info.get_model()
        serial = await robot.robot_info.get_serial_number()
        version = await robot.robot_info.get_version()
        uptime = await robot.robot_info.get_uptime()
        
        print(f"Model:          {model}")
        print(f"Serial Number:  {serial}")
        print(f"Version:        {version}")
        print(f"Uptime:         {uptime}")
        
        print("\n--- 2. Operational State ---")
        alarms = await robot.robot_info.get_active_alarms()
        servo_state = await robot.robot_info.get_servo_state()
        op_state = await robot.robot_info.get_operation_state()
        mode_state = await robot.robot_info.get_mode_state()
        prog_speed = await robot.robot_info.get_program_speed()
        
        print(f"Active Alarms:  {alarms}")
        print(f"Servo State:    {'ON' if servo_state else 'OFF'}")
        print(f"Op State (Raw): {op_state}")
        print(f"Mode State:     {mode_state}")
        print(f"Program Speed:  {prog_speed}%")

        print("\n--- 3. Motion & Position (ns=2) ---")
        try:
            position = await robot.robot_info.get_position()
            print(f"Position Data:  {position}")
        except Exception as e:
            print(f"Position Error: {e}")
            
        try:
            torque = await robot.robot_info.get_torque()
            print(f"Torque Data:    {torque}")
        except Exception as e:
            print(f"Torque Error:   {e}")

        print("\n--- 4. Discrete I/O (Modbus ns=1) ---")
        try:
            # Test getting Digital Input 1
            di_1 = await robot.io.get_digital_input(1)
            print(f"DI[1] State:    {di_1}")
            
            # Test getting Digital Output 1
            do_1 = await robot.io.get_digital_output(1)
            print(f"DO[1] State:    {do_1}")
        except Exception as e:
            print(f"I/O Error (May not be mapped in RoboGuide): {e}")

if __name__ == "__main__":
    asyncio.run(main())
