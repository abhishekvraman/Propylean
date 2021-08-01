import pytest
import pandas as pd

from propylean import streams

def test_energy_stream_instantiation():
    energy = streams.energy_stream()
    assert energy.value == 0
    assert energy.unit == 'kW'
    energy = streams.energy_stream(10, 'MW')
    assert energy.value == 10
    assert energy.unit == 'MW'
    with pytest.raises(Exception):
        en = streams.energy_stream(10, 'Barrels of oil per day')

def test_energy_stream_value_in_other_unit_getter():
    energy = streams.energy_stream(10, 'MW')
    assert energy.get_value_in('W')== 10000000
    assert abs(energy.get_value_in('BTU/h') - 34121416.331279) <0.0001
    assert abs(energy.get_value_in('hp') - 13596.21617304) <0.0001
    with pytest.raises(Exception):
        en = energy.get_value_in('Barrels of oil per day')

    energy = streams.energy_stream(25000000, 'cal/s')
    assert abs(energy.get_value_in('GWh/d') - 2.5120) <0.0001
    
    
