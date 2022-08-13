import pytest
import pandas as pd

from propylean import properties

@pytest.mark.positive
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

@pytest.mark.negative
def test_Length_incorrect_instantiation():
    with pytest.raises(Exception):
        l = properties.Length(10, 'nauticle miles')

@pytest.mark.positive
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
    
@pytest.mark.negative
def test_Time_incorrect_instantiation():
    with pytest.raises(Exception):
            t = properties.Time(10, 'decade')

@pytest.mark.positive
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
    
@pytest.mark.negative
def test_Pressure_incorrect_instantiation_conversion():
    with pytest.raises(Exception):
        pressure = properties.Pressure(value=101325, unit = 'K')
    with pytest.raises(Exception):
        pressure = properties.Pressure(value=101325)
        pressure.unit = 'atmosphere'

@pytest.mark.positive
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
    assert abs(temp.value -422.039) < 0.01

    temp = properties.Temperature(value=2000, unit='R')
    temp.unit = 'C'
    assert abs(temp.value - 837.9611) < 0.0001
   
@pytest.mark.negative
def test_Temperature_incorrect_instantiation_conversion():
    with pytest.raises(Exception):
        temp = properties.Temperature(value=300, unit='Pa')

    with pytest.raises(Exception):
        temp = properties.Temperature(value=300)
        temp.unit = 'Pa'

@pytest.mark.positive
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

@pytest.mark.negative
def test_MassFlowRate_incorrect_instantiatio_conversion():
    with pytest.raises(Exception):
        mfr = properties.MassFlowRate(value=10, unit='Mg/h')
    
    with pytest.raises(Exception):
        mfr = properties.MassFlowRate(value=10)
        mfr.unit = 'lb/mn'

@pytest.mark.positive
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

@pytest.mark.negative
def test_MolarFlowRate_incorrect_instantiation_conversion():
    with pytest.raises(Exception):
        mfr = properties.MolarFlowRate(value=10, unit='gmol/h')
    
    with pytest.raises(Exception):
        mfr = properties.MolarFlowRate(value=10)
        mfr.unit = 'lb/mn'

@pytest.mark.positive
def test_VolumeFlowRate_instantiation_conversion():
    vf = properties.VolumetricFlowRate(10)
    assert vf.value == 10
    assert vf.unit == 'm^3/s'
    vf.unit = 'gal/min'
    assert abs(vf.value - 158502.972) < 1
    vf = properties.VolumetricFlowRate(100, 'lit/h')
    assert vf.unit == 'lit/h'
    vf.unit = 'ft^3/d'
    assert abs(vf.value-84.7553) < 0.01

@pytest.mark.negative
def test_VolumeFlowRate_incorrect_instantiation_conversion():
    with pytest.raises(Exception):
        vf = properties.VolumetricFlowRate(value=10, unit='gmol/h')
    
    with pytest.raises(Exception):
        vf = properties.VolumetricFlowRate(value=10)
        vf.unit = 'pints per day'

@pytest.mark.positive
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

    power = properties.Power(25000000, 'cal/s')
    power.unit = 'GWh/d'
    assert abs(power.value - 2.5120) <0.0001

@pytest.mark.negative
def test_Power_instantiation_conversion():
    with pytest.raises(Exception):
        power = properties.Power(10000000, 'Barrels of oil per day')
    with pytest.raises(Exception):
        power = properties.Power(value=10000000)
        power.unit = 'Barrels of oil per day'

@pytest.mark.positive
def test_property_density():
    d1 = properties.Density(1000)
    assert d1.value == 1000
    assert d1.unit == "kg/m^3"
    d1.unit = "lbm/ft^3"
    assert abs(d1.value-62.479) < 0.01

@pytest.mark.positive
def test_property_dviscosity():
    dv1 = properties.DViscosity(0.000902688)
    assert dv1.value == 0.000902688
    assert dv1.unit == "Pa-s"
    dv1.unit = "cP"
    assert abs(dv1.value-0.902688) < 0.001

@pytest.mark.addition
def test_property_addition():
    p1 = properties.Pressure(1, 'bar')
    p2 = properties.Pressure(2, 'bar')
    p3 = p1 + p2
    assert p3.value == 3
    assert p3.unit == 'bar'

    p1 = properties.Pressure()
    p2 = properties.Pressure(2, 'atm')
    p3 = p1 + p2
    assert p3.value == 303965.0
    assert p3.unit == 'Pa'

    m1 = properties.MassFlowRate(2)
    m2 = properties.MassFlowRate(3)
    m3 = m1 + m2
    assert isinstance(m1, properties.MassFlowRate)
    assert isinstance(m3, properties.MassFlowRate)

@pytest.mark.subtraction
def test_property_subtraction():
    p1 = properties.Pressure(1, 'bar')
    p2 = properties.Pressure(2, 'bar')
    p3 = p2 - p1
    assert p3.value == 1
    assert p3.unit == 'bar'

    p1 = properties.Pressure()
    p2 = properties.Pressure(2, 'atm')
    p3 = p2 - p1
    assert (p3.value - 1)<0.01
    assert p3.unit == 'atm'
    assert p3 == p2 - p1

@pytest.mark.positive
def test_property_equality():
    l1 = properties.Length(2,'m')
    l2 = properties.Length(2000, 'mm')
    assert l1==l2

def test_property_same_not_equal():
    l1 = properties.Length(2,'m')
    l2 = properties.Length(200, 'mm')
    assert not l1==l2

def test_property_different_not_equal():
    t = properties.Temperature()
    m = properties.MassFlowRate()
    assert not t==m

@pytest.mark.positive
@pytest.mark.time_series
def test_propert_time_series_passed_series():
    p = properties._Property()
    idx = pd.date_range("2018-01-01", periods=5, freq="H")
    ts = pd.Series(range(len(idx)), index=idx)
    p.time_series = ts
    assert ts.equals(p.time_series)
    assert p.time_series.equals(ts)

@pytest.mark.positive
@pytest.mark.time_series
def test_propert_time_series_passed_dataframe():
    p = properties._Property()
    idx = pd.date_range("2018-01-01", periods=5, freq="H")
    ts = pd.DataFrame(range(len(idx)), index=idx)
    p.time_series = ts
    assert ts[0].equals(p.time_series)
    assert p.time_series.equals(ts[0])

    ts_2 = pd.DataFrame({0:idx, 1:range(len(idx))})

    p.time_series = ts_2
    
    assert ts[0].equals(p.time_series)
    assert p.time_series.equals(ts[0])

@pytest.mark.positive
@pytest.mark.time_series
def test_propert_time_series_passed_dict():
    p = properties._Property()
    idx = pd.date_range("2018-01-01", periods=5, freq="H")
    ts = pd.Series(range(len(idx)), index=idx)

    data_dict = {}
    for i in range(len(idx)):
        data_dict[idx[i]] = i
    p.time_series = data_dict
    assert ts.equals(p.time_series)
    assert p.time_series.equals(ts)