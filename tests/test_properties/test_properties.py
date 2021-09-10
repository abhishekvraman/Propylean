import pytest
import pandas as pd

from propylean import properties

def test_Length_instantiation_conversion():
    l = properties.Length()
    assert l.value == 0
    assert l.unit == 'm'
    l.value = 1000
    l.unit = 'mm'
    assert l.value == 1000000
    l = properties.Length(value = 1000, unit='foot')
    l.unit = 'yard'
    assert (l.value - 333.333333) < 0.00001
    with pytest.raises(Exception):
        l = properties.Length(10, 'nauticle miles')

def test_Time_instantiation_conversion():
    t = properties.Time()
    assert t.value == 0
    assert t.unit == 'sec'
    t.value = 3600
    t.unit = 'hour'
    assert t.value == 1
    t = properties.Time(value = 1, unit='year')
    t.unit = 'month'
    assert (t.value - 12) < 0.00001
    with pytest.raises(Exception):
        t = properties.Time(10, 'decade')

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
    with pytest.raises(Exception):
        pressure = properties.Pressure(value=101325, unit = 'K')
    with pytest.raises(Exception):
        pressure = properties.Pressure(value=101325)
        pressure.unit = 'atmosphere'

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
    with pytest.raises(Exception):
        temp = properties.Temperature(value=300, unit='Pa')

    with pytest.raises(Exception):
        temp = properties.Temperature(value=300)
        temp.unit = 'Pa'

def test_MassFlowRate_instantiation_conversion():
    mfr = properties.MassFlowRate(value=10)
    mfr.unit = 'g/s'
    assert mfr.value == 10000
    mfr = properties.MassFlowRate(value=10)
    assert mfr.value == 10
    assert mfr.unit == 'kg/s'
    mfr.unit = 'lb/min'
    assert abs(mfr.value - 1322.77) <= 1
    mfr = properties.MassFlowRate(value=10, unit='ton/d') # changed to 10 ton/d
    assert mfr.unit == 'ton/d'
    mfr.value = 100 #changed to 100 ton/day
    mfr.unit = 'kg/h' # changed unit to see new value
    assert abs(mfr.value - 4166.68) < 0.1

    with pytest.raises(Exception):
        mfr = properties.MassFlowRate(value=10, unit='Mg/h')
    
    with pytest.raises(Exception):
        mfr = properties.MassFlowRate(value=10)
        mfr.unit = 'lb/mn'

def test_MolarFlowRate_instantiation_conversion():
    mfr = properties.MolarFlowRate(value=10)
    assert mfr.value == 10
    assert mfr.unit == 'mol/s'
    mfr.unit = 'lbmol/h'
    assert abs(mfr.value - 79.3664) <= 0.01
    mfr = properties.MolarFlowRate(value=10, unit='kmol/d') # changed to 10 ton/d
    assert mfr.unit == 'kmol/d'
    mfr.value = 100 #changed to 100 kmol/day
    mfr.unit = 'lbmol/min' # changed unit to see new value
    assert abs(mfr.value - 9.18593/60) < 0.5

    with pytest.raises(Exception):
        mfr = properties.MolarFlowRate(value=10, unit='gmol/h')
    
    with pytest.raises(Exception):
        mfr = properties.MolarFlowRate(value=10)
        mfr.unit = 'lb/mn'

def test_Power_instantiation_conversion():
    power = properties.Power()
    assert power.value == 0
    assert power.unit == 'W'
    power = properties.Power(10, 'MW')
    assert power.value == 10
    assert power.unit == 'MW'
    with pytest.raises(Exception):
        en = properties.Power(10, 'Barrels of oil equivalent per day')
    
    power = properties.Power(value=10000000)
    assert power.value == 10000000
    power.unit = 'BTU/h'
    assert abs(power.value - 34121416.331279) <0.0001
    power.unit = 'hp'
    assert abs(power.value - 13596.21617304) <0.0001
    with pytest.raises(Exception):
        power.unit = 'Barrels of oil per day'

    power = properties.Power(25000000, 'cal/s')
    power.unit = 'GWh/d'
    assert abs(power.value - 2.5120) <0.0001