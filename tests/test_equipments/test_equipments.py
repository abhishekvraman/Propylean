import pytest
import pandas as pd
from propylean.equipments import CentrifugalPump, PipeSegment, ControlValve, CentrifugalCompressor
from propylean.equipments import get_equipment_index 
from propylean import streams


@pytest.mark.instantiation
def test_CentrifugalPump_instantiation():
    cp = CentrifugalPump(inlet_pressure=50, 
                                     design_pressure = 50,
                                     pressure_drop=-60)
    assert cp.suction_pressure.value == 50
    assert cp.outlet_pressure.value == 110
    assert cp.discharge_pressure.value == 110
    assert cp.discharge_pressure.unit == 'Pa'
    cp.discharge_pressure = 90
    assert cp.outlet_pressure.value == 90
    cp.inlet_mass_flowrate = 10
    assert cp.pressure_drop == -60
    assert cp.differential_pressure == 60
    assert cp.inlet_pressure.value == 30
    cp.differential_pressure = 50
    assert cp.discharge_pressure.value == 80
    
    with pytest.raises(Exception):
        cp.efficiency = -1
    cp.efficiency = 0.6
    assert cp.efficiency == 0.6
    cp.efficiency = 80
    assert cp.efficiency == 0.8
    cp.inlet_mass_flowrate = 20
    assert cp.inlet_mass_flowrate == 20
    if not cp.dynamic_state:
        assert cp.outlet_mass_flowrate == 20
    cp.outlet_mass_flowrate = 30
    if not cp.dynamic_state:
        assert cp.inlet_mass_flowrate == 30
    assert cp.head ==  cp.differential_pressure/(9.8*1000) #unpdate based on liquid density from stream
    
    cp.pump_curve = pd.DataFrame([{'flow':[2,10,30,67], 'head':[45,20,10,2]}])
    with pytest.raises(Exception):
        cp.pump_curve = pd.DataFrame([{'flow':[2,10,30,67], 'head':[45,20,10,2],'something':[2,3,4]}])
        cp.pump_curve = [[2,10,30,67],[45,20,10,2]]

    del cp

@pytest.mark.instantiation
def test_CentrifugalPump_wrong_instantiation():
    with pytest.raises(Exception):
        cp = CentrifugalPump(suction_pressure = 30,
                                        discharge_pressure = 40,
                                        differential_pressure = 10)
    with pytest.raises(Exception):
        cp = CentrifugalPump(suction_pressure = 30,
                                        discharge_pressure = 40,
                                        performance_curve = pd.DataFrame([{'flow':[2,10,30,67], 'head':[45,20,10,2]}]))
    with pytest.raises(Exception):
        cp = CentrifugalPump(suction_pressure = 30,
                                        differential_pressure = 10,
                                        performance_curve = pd.DataFrame([{'flow':[2,10,30,67], 'head':[45,20,10,2]}]))
    with pytest.raises(Exception):
        cp = CentrifugalPump(discharge_pressure = 40,
                                        differential_pressure = 10,
                                        performance_curve = pd.DataFrame([{'flow':[2,10,30,67], 'head':[45,20,10,2]}]))

@pytest.mark.instantiation
def test_PipeSegment_instantiation():
    p = PipeSegment(thickness=2, OD=15, length = 10)
    assert p.ID == 13
    
    #Raise exception if ID is not calculatable or explicitly defined
    with pytest.raises(Exception):
            p = PipeSegment(thickness=2, length = 10)
    
    #Raise exception if length is not defined in case of straight segement as it is a default type
    with pytest.raises(Exception):
        p = PipeSegment(thickness=2, ID=15)
    
    #Raise exception if segment is not in range of the list or material is not in range of the list
    with pytest.raises(Exception):
        p = PipeSegment(thickness=2, ID=15, segment_type = 30, material = 22)
    
    # Do not raise exception if length is not defined but segement is not straight pipe
    try:
        p = PipeSegment(ID=15, segment_type = 6)
    except Exception as exc:
        assert False, f"'Ball valve instantiation' raised an exception {exc}"

@pytest.mark.pressure_drop
def test_PipeSegment_pressure_drop():
    p = PipeSegment(ID=0.018, OD=0.020, length = 10) # in meters 
    p.inlet_pressure = 1.053713e7  #Pascal
    p.inlet_temperature = 298.17 #degree Celsius
    p.inlet_mass_flowrate = 1   #kg/s
    assert p.inlet_mass_flowrate != None
    assert p.ID != None
    assert p.outlet_pressure != None
    assert abs(p.pressure_drop - 115555)<150000 #Pa  NEEDS UPDATE !!!!!

@pytest.mark.printing
def test_PipeSegment_print(capsys):
    pipe = PipeSegment(tag='Pump_1_Inlet', length=100, ID=2)
    print(pipe)
    captured = capsys.readouterr()
    assert captured.out == 'Pipe Segment with tag: Pump_1_Inlet\n'

@pytest.mark.instantiation
def test_ControlValve_instantiation():
    #All units in SI
    valve = ControlValve(inlet_pressure=1.04217e7, outlet_pressure=9.92167e6, inlet_temperature=299.18)
    valve.inlet_mass_flowrate = 1 #kg/s
    assert abs(valve.pressure_drop - (1.04217e7-9.92167e6)) < 0.001
    assert abs(valve.Kv - 1.61259) < 0.001

    # Gas phase calculation
    valve = ControlValve(inlet_pressure=202650, outlet_pressure=197650, inlet_temperature=423.15)
    valve.inlet_mass_flowrate = 1 #kg/s
    assert valve.pressure_drop == 5000
    assert abs(valve.Kv - 502.88) <= 118.5 #NEEDS UPDATE 
    del valve

@pytest.mark.instantiation
def test_CentrifugalCompressor_instantiation():
    
    compressor = CentrifugalCompressor(suction_pressure = 1013250.0, #Pa
                                                  differential_pressure = 5000000.0, #Pa
                                                  inlet_temperature = 248.15, #K
                                                  inlet_mass_flowrate = 0.02778) #kg/s
    
    assert compressor.discharge_pressure.value == 1013250.0 + 5000000.0
    
    assert abs(compressor.power - 10.58) < 0.5 # kW

    compressor.polytropic_efficiency = 0.80
    assert abs(compressor.adiabatic_efficiency - 0.766) < 0.1
    assert abs(compressor.power - 9.6698) < 0.5 # kW 

@pytest.mark.listing
def test_listing_of_equipments():
    first_pump = CentrifugalPump(tag='1', inlet_pressure=50, 
                                     design_pressure = 50,
                                     pressure_drop=-60)
    second_pump = CentrifugalPump(tag='2', inlet_pressure=50, 
                                     design_pressure = 50,
                                     pressure_drop=-60)
    third_pump = CentrifugalPump(tag='3', inlet_pressure=50, 
                                     design_pressure = 50,
                                     pressure_drop=-60)
    first_valve = ControlValve(tag='1', inlet_pressure=1.04217e7, outlet_pressure=9.92167e6, inlet_temperature=299.18)
    second_valve = ControlValve(tag='2', inlet_pressure=1.04217e7, outlet_pressure=9.92167e6, inlet_temperature=299.18)
    third_valve = ControlValve(tag='3', inlet_pressure=1.04217e7, outlet_pressure=9.92167e6, inlet_temperature=299.18)
    forth_valve = ControlValve(tag='4', inlet_pressure=1.04217e7, outlet_pressure=9.92167e6, inlet_temperature=299.18)
    fifth_valve = ControlValve(tag='5', inlet_pressure=1.04217e7, outlet_pressure=9.92167e6, inlet_temperature=299.18)
    
    assert first_pump.tag == '1'
    for pump in CentrifugalPump.list_objects():
        assert pump.tag in [None, '1', '2', '3']
  
    for valve in ControlValve.list_objects():
        assert valve.tag in [None, '1', '2', '3', '4', '5']

@pytest.mark.indexing
def test_indexing_of_equipments():
    assert get_equipment_index('1','centrifugal pump') == 1
    control_valve = ControlValve()
    assert len(get_equipment_index(None,'control valves')) == 3
    with pytest.raises(Exception):
        get_equipment_index(None,'Trucks')
    
    assert get_equipment_index('1','pump')==[(1,'Centrifugal Pump'),([],'Positive Displacement Pump')]
    
    search_result = get_equipment_index('2')
    for result in search_result:
        if result[1] in ['Centrifugal Pump', 'Control Valve']:
            assert isinstance(result[0],int)
        else:
            assert isinstance(result[0],list)

@pytest.mark.unique_equipment
def test_no_equipment_with_same_tag_and_type():
    for i in range(10):
        some_pumps = []
        try:
            some_pumps.append([CentrifugalPump(tag='Pump_'+str(i)), CentrifugalPump(tag='Pump_'+str(i+1))])
        except:
            continue
    a = set(CentrifugalPump.list_objects())
    assert len(a) == len(CentrifugalPump.list_objects())

@pytest.mark.connections
def test_equipment_stream_connection():
    s1 = streams.MaterialStream(tag='Pump-inlet')
    s2 = streams.MaterialStream(tag='Pump-outlet')
    en1 = streams.EnergyStream(tag='Pump-power')
    eq1 = CentrifugalPump(tag="P-234")
    eq1.connect_stream(s1,'in')
    assert eq1.get_stream_tag('m', 'in') == 'Pump-inlet'
    eq1.connect_stream(direction='out', stream_tag='Pump-outlet', stream_type='m')
    assert eq1.get_stream_tag('Material', 'out') == 'Pump-outlet'
    eq1.connect_stream(en1)
    assert eq1.get_stream_tag('energy', 'in') == 'Pump-power'