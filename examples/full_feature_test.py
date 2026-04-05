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
            di_1 = await robot.io.get_digital_input(1)
            print(f"DI[1] State:    {di_1}")
            
            do_1 = await robot.io.get_digital_output(1)
            print(f"DO[1] State:    {do_1}")
            
            ui_1 = await robot.io.get_uop_input(1)
            print(f"UI[1] State:    {ui_1}")
            
            flag_1 = await robot.io.get_flag(1)
            print(f"Flag[1] State:  {flag_1}")
        except Exception as e:
            print(f"I/O Error: {e}")

        print("\n--- 5. Registers (Modbus ns=1) ---")
        try:
            gi_1 = await robot.registers.get_group_input(1)
            print(f"GI[1] Value:    {gi_1}")
            
            # Read Holding Register 1 (Usually R[1] by default Fanuc mapping)
            r_1 = await robot.registers.read_holding_register(1, "int16")
            print(f"R[1] (Address 1, int16): {r_1}")
            
            # Read Holding Register 11 (If mapped as a REAL in SNPX_ASG)
            # This requires two registers starting at address 11
            # r_real = await robot.registers.read_holding_register(11, "real")
            # print(f"Address 11 (REAL): {r_real}")
            
        except Exception as e:
            print(f"Register Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
