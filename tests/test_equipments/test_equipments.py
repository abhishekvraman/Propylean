import pytest
import pandas as pd

from propylean import equipments

cp = equipments.centrifugal_pump(inlet_pressure=50, design_pressure = 50, pressure_drop=-60)
def test_centrifugal_pump_instantiation():
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
        cp.pump_curve = pd.DataFrame([{'flow':[2,10,30,67], 'head':[45,20,10,2],'some':[2,3,4]}])
        cp.pump_curve = [[2,10,30,67],[45,20,10,2]]

p = equipments.pipe(thickness=2, OD=15)
def test_pipe():
    assert p.ID == 13

