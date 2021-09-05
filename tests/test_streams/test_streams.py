import pytest
import pandas as pd

from propylean import streams

def test_EnergyStream_instantiation():
    energy = streams.EnergyStream()
    assert energy.value == 0
    assert energy.unit == 'W'
    energy = streams.EnergyStream(10, 'MW')
    assert energy.value == 10
    assert energy.unit == 'MW'
    with pytest.raises(Exception):
        en = streams.EnergyStream(10, 'Barrels of oil per day')

def test_EnergyStream_value_in_other_unit_getter():
    energy = streams.EnergyStream(10, 'MW')
    energy.unit = 'W'
    assert energy.value == 10000000
    energy.unit = 'BTU/h'
    assert abs(energy.value- 34121416.331279) <0.0001
    

 
    
    
