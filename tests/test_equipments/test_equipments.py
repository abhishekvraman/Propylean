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
    assert cp.pressure_drop == -40
    assert cp.differential_pressure == 40
    cp.differential_pressure = 50
    assert cp.suction_pressure == 50
    assert cp.discharge_pressure == 100
    
    with pytest.raises(Exception):
        cp.efficiency = -1
    cp.efficiency = 0.6
    assert cp.efficiency == 0.6
    cp.efficiency = 80
    assert cp.efficiency == 0.8
    cp.inlet_flowrate = 20
    assert cp.inlet_flowrate == 20
    if not cp.dynamic_state:
        assert cp.outlet_flowrate == 20
    cp.outlet_flowrate = 30
    if not cp.dynamic_state:
        assert cp.inlet_flowrate == 30
    assert cp.head ==  cp.differential_pressure/(9.8*1000) #unpdate based on liquid density from stream
    
    cp.pump_curve = pd.DataFrame([{'flow':[2,10,30,67], 'head':[45,20,10,2]}])
    with pytest.raises(Exception):
        cp.pump_curve = pd.DataFrame([{'flow':[2,10,30,67], 'head':[45,20,10,2],'something':[2,3,4]}])
        cp.pump_curve = [[2,10,30,67],[45,20,10,2]]

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

# def test_pipe_segment_pressure_drop():
