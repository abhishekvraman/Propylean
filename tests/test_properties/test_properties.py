import pytest
import pandas as pd

from propylean import properties

def test_Pressure_instantiation_conversion():
    pressure = properties.Pressure(value=101325)
    assert pressure.value == 101325
    assert pressure.unit == 'Pa'
    pressure.unit = 'atm'
    assert abs(pressure.value - 1) <= 0.0001
    pressure = properties.Pressure(value=10, unit='psi') # changed to 10 psi
    assert pressure.unit == 'psi'
    pressure.value = 100 #changed to 100 psi
    pressure.unit = 'mm Hg' # changed unit to see new value
    assert abs(pressure.value - 5171.5) < 1 
    
def test_Temperature_instantiation_conversion():
    temp = properties.Temperature(value=300)
    assert temp.value == 300
    assert temp.unit == 'K'
    temp.unit = 'F'
    assert abs(temp.value - 80.33) < 0.000001
    temp.unit = 'R'
    assert abs(temp.value - 540) < 0.000001

    temp = properties.Temperature(value=300, unit='F')
    temp.unit = 'K'
    assert abs(temp.value -422.039) < 0.001

    temp = properties.Temperature(value=2000, unit='R')
    temp.unit = 'C'
    assert abs(temp.value - 837.9611) < 0.0001

