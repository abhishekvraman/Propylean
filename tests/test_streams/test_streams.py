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
        en = streams.EnergyStream(10, 'Barrels of oil equivalent per day')
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
    
def test_listing_of_streams():
    energy_stream_1 = streams.EnergyStream(tag='ES1')
    energy_stream_2 = streams.EnergyStream(tag='ES2')
    energy_stream_3 = streams.EnergyStream(tag='ES3')
    
    material_streams = []
    for i in range(1,7):
        material_streams.append(streams.MaterialStream(tag='MS_'+str(i)))
    
    assert energy_stream_2.tag=='ES2'

    assert len(streams.EnergyStream.list_objects())!=0
    for es in streams.EnergyStream.list_objects():
        assert es.tag in [None, 'ES1', 'ES2', 'ES3', 'Heat input']
  
    for ms in streams.MaterialStream.list_objects():
        assert ms.tag in [None, 'MS_1', 'MS_2', 'MS_3', 'MS_4', 'MS_5', 'MS_6', 'Input Stream 1']

def test_indexing_of_streams():
    energy_stream_4 = streams.EnergyStream(tag='ES4')
    assert streams.get_stream_index(stream_type='energy',tag='ES4') == 7
    assert len(streams.get_stream_index(stream_type='energy', tag=None)) == 3

    materia_stream_1 = streams.MaterialStream(mass_flow_rate=10,tag='Pump Inlet')
    

    assert streams.get_stream_index(stream_type='material',tag='Pump Inlet') == 8

    materia_stream_3 = streams.MaterialStream(mass_flow_rate=10,tag='ES4')
    assert streams.get_stream_index('ES4')==[(7,'Energy Stream'),(9,'Material Stream')]
    
    material_streams = []
    for i in range(1,11):
        material_streams.append(streams.MaterialStream())
    assert len(streams.get_stream_index(stream_type='material', tag=None)) == 11
    
    with pytest.raises(Exception):
        i = streams.get_stream_index(stream_type='gas', tag=None)

    with pytest.raises(Exception):
        i = streams.get_stream_index('Pump Outlet', 'material')
