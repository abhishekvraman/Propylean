import pytest

from productionplant import equipments

cp = equipments.centrifugal_pump(inlet_pressure=50, design_pressure = 50, pressure_drop=-60)
def test_centrifugal_pump():
    
    assert cp.suction_pressure == 50
    assert cp.outlet_pressure == 110
    assert cp.discharge_pressure == 110
    cp.outlet_pressure = 90
    assert cp.outlet_pressure == 90
    assert cp.pressure_drop == -40
    assert cp.differential_pressure == 40
    cp.differential_pressure = 50
    assert cp.inlet_pressure == 50
    assert cp.outlet_pressure == 100
    
    with pytest.raises(Exception):
        cp.efficiency = -1
    cp.efficiency = 0.6
    assert cp.efficiency == 0.6
    assert cp.efficiency == 0.6
    cp.efficiency = 80
    assert cp.efficiency == 0.8
    cp.inlet_flowrate = 20
    assert cp.inlet_flowrate == 20
    assert cp.outlet_flowrate == 20
    assert cp.head ==  cp.differential_pressure/(9.8*1000)


p = equipments.pipe(thickness=2, OD=15)
def test_pipe():
    assert p.ID == 13

