from fanuc_opcua.nodes import NodeKeys, ModbusNodes

def test_node_keys():
    assert NodeKeys.ALARM == "ns=2;s=Alarm"
    assert NodeKeys.MODEL == "ns=2;s=Model"
    
def test_modbus_nodes():
    assert ModbusNodes.DISCRETE_INPUT == "ns=1;i=301"
    assert ModbusNodes.HOLDING_REGISTERS == "ns=1;i=304"
