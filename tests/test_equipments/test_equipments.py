import pytest
import pandas as pd

from propylean import equipments


def test_centrifugal_pump_instantiation():
    cp = equipments.centrifugal_pump(inlet_pressure=50, 
                                     design_pressure = 50,
                                     pressure_drop=-60)
    assert cp.suction_pressure == 50
    assert cp.outlet_pressure == 110
    assert cp.discharge_pressure == 110
    cp.discharge_pressure = 90
    assert cp.outlet_pressure == 90
    cp.inlet_mass_flowrate = 10
    assert cp.pressure_drop == -60
    assert cp.differential_pressure == 60
    assert cp.inlet_pressure == 30
    cp.differential_pressure = 50
    assert cp.discharge_pressure == 80
    
    with pytest.raises(Exception):
        cp.efficiency = -1
    cp.efficiency = 0.6
    assert cp.efficiency == 0.6
    cp.efficiency = 80
    assert cp.efficiency == 0.8
    cp.inlet_mass_flowrate = 20
    assert cp.inlet_mass_flowrate == 20
    if not cp.dynamic_state:
        assert cp.outlet_mass_flowrate == 20
    cp.outlet_mass_flowrate = 30
    if not cp.dynamic_state:
        assert cp.inlet_mass_flowrate == 30
    assert cp.head ==  cp.differential_pressure/(9.8*1000) #unpdate based on liquid density from stream
    
    cp.pump_curve = pd.DataFrame([{'flow':[2,10,30,67], 'head':[45,20,10,2]}])
    with pytest.raises(Exception):
        cp.pump_curve = pd.DataFrame([{'flow':[2,10,30,67], 'head':[45,20,10,2],'something':[2,3,4]}])
        cp.pump_curve = [[2,10,30,67],[45,20,10,2]]

    del cp

def test_centrifugal_pump_wrong_instantiation():
    with pytest.raises(Exception):
        cp = equipments.centrifugal_pump(suction_pressure = 30,
                                         discharge_pressure = 40,
                                         differential_pressure = 10)
    with pytest.raises(Exception):
        cp = equipments.centrifugal_pump(suction_pressure = 30,
                                         discharge_pressure = 40,
                                         performance_curve = pd.DataFrame([{'flow':[2,10,30,67], 'head':[45,20,10,2]}]))
    with pytest.raises(Exception):
        cp = equipments.centrifugal_pump(suction_pressure = 30,
                                         differential_pressure = 10,
                                         performance_curve = pd.DataFrame([{'flow':[2,10,30,67], 'head':[45,20,10,2]}]))
    with pytest.raises(Exception):
        cp = equipments.centrifugal_pump(discharge_pressure = 40,
                                         differential_pressure = 10,
                                         performance_curve = pd.DataFrame([{'flow':[2,10,30,67], 'head':[45,20,10,2]}]))

def test_pipe_segment_instantiation():
    p = equipments.pipe_segment(thickness=2, OD=15, length = 10)
    assert p.ID == 13
    
    #Raise exception if ID is not calculatable or explicitly defined
    with pytest.raises(Exception):
            p = equipments.pipe_segment(thickness=2, length = 10)
    
    #Raise exception if length is not defined in case of straight segement as it is a default type
    with pytest.raises(Exception):
        p = equipments.pipe_segment(thickness=2, ID=15)
    
    #Raise exception if segment is not in range of the list or material is not in range of the list
    with pytest.raises(Exception):
        p = equipments.pipe_segment(thickness=2, ID=15, segment_type = 30, material = 22)
    
    # Do not raise exception if length is not defined but segement is not straight pipe
    try:
        p = equipments.pipe_segment(ID=15, segment_type = 6)
    except Exception as exc:
        assert False, f"'Ball valve instantiation' raised an exception {exc}"

def test_pipe_segment_pressure_drop():
    p = equipments.pipe_segment(ID=18, OD=20, length = 10) #ID in mm, OD in mm and length in meters 
    p.inlet_pressure = 1.053713e7  #Pascal
    p.inlet_temperature = 25 #degree Celsius
    p.inlet_mass_flowrate = 1   #kg/s
    assert p.inlet_mass_flowrate != None
    assert p.ID != None
    assert p.outlet_pressure != None
    assert abs(p.pressure_drop - 1.154)<0.01 #Bar

def test_control_valve_instantiation():
    #All units in SI
    valve = equipments.control_valve(inlet_pressure=1.04217e7, outlet_pressure=9.92167e6, inlet_temperature=299.18)
    valve.inlet_mass_flowrate = 1 #kg/s
    assert abs(valve.pressure_drop - (1.04217e7-9.92167e6)) < 0.001
    assert abs(valve.Kv - 1.61259) < 0.001

    # Gas phase calculation
    valve = equipments.control_valve(inlet_pressure=202650, outlet_pressure=197650, inlet_temperature=423.15)
    valve.inlet_mass_flowrate = 1 #kg/s
    assert abs(valve.Kv - 502.88) < 50 #NEEDS UPDATE 

    del valve
def test_centrifugal_compressor_instantiation():
    
    compressor = equipments.centrifugal_compressors(suction_pressure = 1013250.0, #Pa
                                                    differential_pressure = 5000000.0, #Pa
                                                    inlet_temperature = 248.15, #K
                                                    inlet_mass_flowrate = 0.02778) #kg/s
    
    assert compressor.discharge_pressure == 1013250.0 + 5000000.0
    
    assert abs(compressor.power - 10.58) < 0.5 # kW

    compressor.polytropic_efficiency = 0.80
    assert abs(compressor.adiabatic_efficiency - 0.766) < 0.1
    assert abs(compressor.power - 9.6698) < 0.5 # kW 

def test_listing_of_equipments():
    first_pump = equipments.centrifugal_pump(tag='1', inlet_pressure=50, 
                                     design_pressure = 50,
                                     pressure_drop=-60)
    second_pump = equipments.centrifugal_pump(tag='2', inlet_pressure=50, 
                                     design_pressure = 50,
                                     pressure_drop=-60)
    third_pump = equipments.centrifugal_pump(tag='3', inlet_pressure=50, 
                                     design_pressure = 50,
                                     pressure_drop=-60)
    first_valve = equipments.control_valve(tag='1', inlet_pressure=1.04217e7, outlet_pressure=9.92167e6, inlet_temperature=299.18)
    second_valve = equipments.control_valve(tag='2', inlet_pressure=1.04217e7, outlet_pressure=9.92167e6, inlet_temperature=299.18)
    third_valve = equipments.control_valve(tag='3', inlet_pressure=1.04217e7, outlet_pressure=9.92167e6, inlet_temperature=299.18)
    forth_valve = equipments.control_valve(tag='4', inlet_pressure=1.04217e7, outlet_pressure=9.92167e6, inlet_temperature=299.18)
    fifth_valve = equipments.control_valve(tag='5', inlet_pressure=1.04217e7, outlet_pressure=9.92167e6, inlet_temperature=299.18)
    
    assert first_pump.tag == '1'
    for pump in equipments.centrifugal_pump.list_objects():
        print(pump.tag)
        assert pump.tag in [None, '1', '2', '3']

        
    for valve in equipments.control_valve.list_objects():
        assert valve.tag in [None, '1', '2','3', '4', '5']
