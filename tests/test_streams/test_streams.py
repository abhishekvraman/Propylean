import pytest
import pandas as pd
from propylean.streams import EnergyStream, MaterialStream
from propylean.streams import get_stream_index
from propylean.equipments import ControlValve

@pytest.mark.instantiation
def test_EnergyStream_instantiation():
    energy = EnergyStream()
    assert energy.value == 0
    assert energy.unit == 'W'
    energy = EnergyStream(10, 'MW')
    assert energy.value == 10
    assert energy.unit == 'MW'
    with pytest.raises(Exception):
        en = EnergyStream(10, 'Barrels of oil equivalent per day')
    energy = EnergyStream(10, 'MW')
    energy.unit = 'W'
    assert energy.value == 10000000
    energy.unit = 'BTU/h'
    assert abs(energy.value- 34121416.331279) <0.0001

@pytest.mark.printing
def test_EnergyStream_print(capsys):
    energy = EnergyStream(tag='Heat input')
    print(energy)
    captured = capsys.readouterr()
    assert captured.out == 'Energy Stream Tag: Heat input\n'

@pytest.mark.instantiation
def test_MaterialStream_instantiation():
    MS_1 = MaterialStream()
    assert MS_1.mass_flowrate.value == 0
    assert MS_1.mass_flowrate.unit == 'kg/s'
    assert MS_1.temperature.value == 298
    assert MS_1.temperature.unit == 'K'
    assert MS_1.pressure.value == 101325
    assert MS_1.pressure.unit == 'Pa'

@pytest.mark.printing
def test_MaterialStream_print(capsys):
    ms = MaterialStream(tag='Input Stream 1')
    print(ms)
    captured = capsys.readouterr()
    assert captured.out == 'Material Stream Tag: Input Stream 1\n'

@pytest.mark.listing    
def test_listing_of_streams():
    energy_stream_1 = EnergyStream(tag='ES1')
    energy_stream_2 = EnergyStream(tag='ES2')
    energy_stream_3 = EnergyStream(tag='ES3')
    
    material_streams = []
    for i in range(1,7):
        material_streams.append(MaterialStream(tag='MS_'+str(i)))
    
    assert energy_stream_2.tag=='ES2'

    assert len(EnergyStream.list_objects())!=0
    for es in EnergyStream.list_objects():
        assert es.tag in [None, 'ES1', 'ES2', 'ES3', 'Heat input', 'Pump-power']
  
    for ms in MaterialStream.list_objects():
        assert ms.tag in [None, 'MS_1', 'MS_2', 'MS_3', 'MS_4', 'MS_5', 'MS_6',\
                         'Input Stream 1', '1', '2', 'Pump-inlet', 'Pump-outlet', \
                         'Pump-inlet_1', 'Pump-outlet_2']

@pytest.mark.indexing
def test_indexing_of_streams():
    energy_stream_4 = EnergyStream(tag='ES4')
    assert (get_stream_index(stream_type='energy',tag='ES4') == 10 or
            get_stream_index(stream_type='energy',tag='ES4') == 9) #change number if add/remove energy stream 
    assert len(get_stream_index(stream_type='energy', tag=None)) == 3

    materia_stream_1 = MaterialStream(mass_flowrate=10,tag='Pump Inlet')
    

    assert (get_stream_index(stream_type='material',tag='Pump Inlet') == 8 or
            get_stream_index(stream_type='material',tag='Pump Inlet') == 12) #change number if add/remove material stream

    materia_stream_3 = MaterialStream(mass_flowrate=10,tag='ES4')
    assert (get_stream_index('ES4')==[(9,'Energy Stream'),(13,'Material Stream')] or
            get_stream_index('ES4')==[(9,'Energy Stream'),(11,'Material Stream')]) #change number if add/remove material stream
    
    material_streams = []
    for i in range(1,11):
        material_streams.append(MaterialStream())
    assert len(get_stream_index(stream_type='material', tag=None)) == 11
    
    with pytest.raises(Exception):
        i = get_stream_index(stream_type='gas', tag=None)

    with pytest.raises(Exception):
        i = get_stream_index('Pump Outlet', 'material')

@pytest.mark.connections
def test_stream_equipment_connection():
    e1 = ControlValve(tag="CV1")
    s1 = MaterialStream(tag='1', to_equipment_tag=e1.tag,
                                to_equipment_type=type(e1))