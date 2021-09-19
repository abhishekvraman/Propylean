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
    energy = streams.EnergyStream(10, 'MW')
    energy.unit = 'W'
    assert energy.value == 10000000
    energy.unit = 'BTU/h'
    assert abs(energy.value- 34121416.331279) <0.0001
def test_EnergyStream_print(capsys):
    energy = streams.EnergyStream(tag='Heat input')
    print(energy)
    captured = capsys.readouterr()
    assert captured.out == 'Energy Stream Tag: Heat input\n'

def test_MaterialStream_instantiation():
    MS_1 = streams.MaterialStream()
    assert MS_1.mass_flow_rate.value == 0
    assert MS_1.mass_flow_rate.unit == 'kg/s'
    assert MS_1.temperature.value == 298
    assert MS_1.temperature.unit == 'K'
    assert MS_1.pressure.value == 101325
    assert MS_1.pressure.unit == 'Pa'
def test_MaterialStream_print(capsys):
    ms = streams.MaterialStream(tag='Input Stream 1')
    print(ms)
    captured = capsys.readouterr()
    assert captured.out == 'Material Stream Tag: Input Stream 1\n'
    
    
