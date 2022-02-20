from fluids.two_phase_voidage import Turner_Wallis
import pytest
import pandas as pd
from thermo import temperature
from propylean.equipments import CentrifugalPump, PipeSegment, ControlValve, CentrifugalCompressor
from propylean.equipments import get_equipment_index 
from propylean import streams, properties


@pytest.mark.instantiation
def test_CentrifugalPump_instantiation():
    cp = CentrifugalPump(tag = "edcqe", pressure_drop=-60)
    cp.inlet_pressure = 50
    cp.pressure_drop = -60
    assert cp.inlet_pressure.value == 50
    assert cp.suction_pressure.value == 50
    assert cp.differential_pressure.value == 60
    assert cp.pressure_drop.value == -60
    assert cp.outlet_pressure.value == 110
    assert cp.discharge_pressure.value == 110
    assert cp.discharge_pressure.unit == 'Pa'
    cp.discharge_pressure = 90
    assert cp.discharge_pressure.value == 90
    assert cp.outlet_pressure.value == 90
    cp.inlet_mass_flowrate = 10
    assert cp.inlet_mass_flowrate.value == 10
    assert cp.outlet_mass_flowrate.value == 10
    assert cp.inlet_pressure.value == 30
    assert cp.suction_pressure.value == 30
    assert cp.differential_pressure.value == 60
    
    cp.differential_pressure = 50
    assert cp.differential_pressure.value == 50
    assert cp.pressure_drop.value == -50
    assert cp.discharge_pressure.value == 80
    assert cp.outlet_pressure.value == 80
    
    with pytest.raises(Exception):
        cp.efficiency = -1
    cp.efficiency = 0.6
    assert cp.efficiency == 0.6
    cp.efficiency = 80
    assert cp.efficiency == 0.8
    cp.inlet_mass_flowrate = 20
    assert cp.inlet_mass_flowrate == properties.MassFlowRate(20)
    if not cp.dynamic_state:
        assert cp.outlet_mass_flowrate == properties.MassFlowRate(20)
    cp.outlet_mass_flowrate = properties.MassFlowRate(30)
    if not cp.dynamic_state:
        assert cp.inlet_mass_flowrate == properties.MassFlowRate(30)
    assert cp.head ==  cp.differential_pressure.value/(9.8*1000) #unpdate based on liquid density from stream
    
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

    assert p.inlet_mass_flowrate.value == 1
    assert p.ID == 0.018
    assert p.inlet_pressure.value == 1.053713e7
    assert p.outlet_pressure.value == p.inlet_pressure.value - p.pressure_drop.value
    assert abs(p.pressure_drop.value - 115555)<15000 #Pa  NEEDS UPDATE !!!!!

@pytest.mark.printing
def test_PipeSegment_print(capsys):
    pipe = PipeSegment(tag='Pump_1_Inlet', length=100, ID=2)
    print(pipe)
    captured = capsys.readouterr()
    assert captured.out == 'Pipe Segment with tag: Pump_1_Inlet\n'

@pytest.mark.instantiation
def test_ControlValve_instantiation():
    #All units in SI
    valve = ControlValve()
    valve.inlet_pressure=1.04217e7
    valve.pressure_drop=1.04217e7 - 9.92167e6
    valve.inlet_temperature=299.18
    valve.inlet_mass_flowrate = 1 #kg/s
    assert valve.inlet_pressure.value == 1.04217e7
    assert valve.outlet_pressure.value == 9.92167e6 
    assert abs(valve.pressure_drop.value - (1.04217e7-9.92167e6)) < 0.001
    assert abs(valve.Kv - 1.61259) < 0.001

    # Gas phase calculation
    valve = ControlValve()
    valve.inlet_pressure = 202650
    valve.pressure_drop = 202650-197650
    valve.inlet_temperature = 423.15
    assert valve.inlet_pressure.value == 202650
    assert valve.outlet_pressure.value == 197650
    assert valve.pressure_drop.value == (202650 - 197650)
    valve.inlet_mass_flowrate = 1 #kg/s
    assert valve.pressure_drop.value == 5000
    assert abs(valve.Kv - 502.88) <= 118.5 #NEEDS UPDATE 
    del valve

@pytest.mark.instantiation
def test_CentrifugalCompressor_instantiation():
    
    compressor = CentrifugalCompressor() 
    compressor.suction_pressure = 1013250.0 #Pa
    compressor.differential_pressure = 5000000.0 #Pa
    compressor.inlet_temperature = 248.15 #K
    compressor.inlet_mass_flowrate = 0.02778#kg/s
    
    assert compressor.discharge_pressure.value == 1013250.0 + 5000000.0
    
    assert abs(compressor.power - 10.58) < 0.8 # kW

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
    assert CentrifugalPump.get_equipment_index('1') == 1
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
def test_equipment_stream_connection_disconnection():
    s1 = streams.MaterialStream(tag='Pump-inlet')
    s2 = streams.MaterialStream(tag='Pump-outlet')
    en1 = streams.EnergyStream(tag='Pump-power')
    eq1 = CentrifugalPump(tag="P-234")
    assert eq1.connect_stream(s1,'in') is True
    assert eq1.get_stream_tag('m', 'in') == 'Pump-inlet'
    assert eq1.connect_stream(direction='out', stream_tag='Pump-outlet', stream_type='m') is True
    assert eq1.get_stream_tag('Material', 'out') == 'Pump-outlet'
    assert eq1.connect_stream(en1) is True
    assert eq1.get_stream_tag('energy', 'in') == 'Pump-power'


    #Checking disconnection
    assert eq1.disconnect_stream(s1) is True
    assert eq1.get_stream_tag('m', 'in') is None
    assert eq1.disconnect_stream(stream_tag='Pump-outlet')
    assert eq1.get_stream_tag('Material', 'out') is None
    assert eq1.disconnect_stream(direction='in', stream_type="energy")
    assert eq1.get_stream_tag('energy', 'in') is None

@pytest.mark.connections
def test_equipment_stream_incorrect_connection_disconnection():
    s1 = streams.MaterialStream(tag='Pump-inlet')
    s2 = streams.MaterialStream(tag='Pump-outlet')
    en1 = streams.EnergyStream(tag='Pump-power')
    eq1 = CentrifugalPump(tag="P-234")
    
    with pytest.raises(Exception):
        result = eq1.connect_stream(s1)
    with pytest.raises(Exception):
        result = eq1.connect_stream(direction='in', stream_type="energy")
    with pytest.raises(Exception):
        result = eq1.connect_stream(s1, direction='North')
    
    assert eq1.connect_stream(s1,'in') is True
    assert eq1.get_stream_tag('m', 'in') == 'Pump-inlet'
    assert eq1.connect_stream(direction='out', stream_tag='Pump-outlet', stream_type='m') is True
    assert eq1.get_stream_tag('Material', 'out') == 'Pump-outlet'
    assert eq1.connect_stream(en1) is True

    with pytest.raises(Exception):
        result = eq1.disconnect_stream(direction='outlet')
    with pytest.raises(Exception):
        result = eq1.disconnect_stream(tag='outlet')

@pytest.mark.property_matching_centrifugal
def test_equipment_stream_properties_matching():
    inlet_pressure = properties.Pressure(10, 'bar')
    outlet_pressure = properties.Pressure(20, 'bar')
    flowrate = properties.MassFlowRate(100, 'kg/s')
    temperature = properties.Temperature(40,'C')

    s1 = streams.MaterialStream(tag='Pump-inlet_1')
    s1.pressure = inlet_pressure
    s1.temperature = temperature
    s1.mass_flowrate = flowrate

    assert s1.pressure == inlet_pressure
    assert s1.temperature == temperature
    assert s1.mass_flowrate == flowrate 

    eq1 = CentrifugalPump(tag="P-24")

    assert eq1.connect_stream(s1, 'in') is True

    assert eq1.inlet_temperature == temperature
    assert eq1.inlet_pressure == inlet_pressure
    assert eq1.inlet_mass_flowrate == flowrate
    assert eq1.outlet_mass_flowrate == flowrate

    s2 = streams.MaterialStream(tag='Pump-outlet_2')
    s2.pressure = outlet_pressure
    s2.temperature = temperature
    s2.mass_flowrate = flowrate

    assert s2.pressure == outlet_pressure
    assert s2.temperature == temperature
    assert s2.mass_flowrate == flowrate
    assert eq1.connect_stream(s2, 'out') is True
    assert eq1.outlet_temperature == temperature
    assert eq1.outlet_pressure == outlet_pressure
    assert eq1.outlet_mass_flowrate == flowrate
    assert eq1.differential_pressure == properties.Pressure(outlet_pressure.value - inlet_pressure.value,
                                                    outlet_pressure.unit)
    assert eq1.pressure_drop == properties.Pressure(-outlet_pressure.value + inlet_pressure.value,
                                                    outlet_pressure.unit)
    en1 = streams.EnergyStream(tag='Pump-power')

@pytest.mark.property_matching_pipesegment
def test_equipment_stream_properties_matching():
    inlet_pressure = properties.Pressure(value=1.053713e7)  #Pascal
    flowrate = properties.MassFlowRate(1, 'kg/s')
    temperature = properties.Temperature(298.17) #degree Celsius

    s1 = streams.MaterialStream(tag='Pipe-inlet_1')
    s1.pressure = inlet_pressure
    s1.temperature = temperature
    s1.mass_flowrate = flowrate

    assert s1.pressure == inlet_pressure
    assert s1.temperature == temperature
    assert s1.mass_flowrate == flowrate 

    eq1 = PipeSegment(tag="P-2344", ID=0.018, OD=0.020, length = 10)

    assert eq1.connect_stream(s1, 'in') is True

    assert eq1.inlet_temperature == temperature
    assert eq1.inlet_pressure == inlet_pressure
    assert eq1.inlet_mass_flowrate == flowrate
    assert eq1.outlet_mass_flowrate == flowrate

    s2 = streams.MaterialStream(tag='Pipe-outlet_2')


    assert eq1.connect_stream(s2, 'out', stream_governed=False) is True
    assert eq1.outlet_temperature == s1.temperature
    assert abs(eq1.outlet_pressure.value - s1.pressure.value + eq1.pressure_drop.value) <100
    assert eq1.outlet_mass_flowrate == s1.mass_flowrate

    assert eq1.outlet_temperature == s2.temperature
    assert eq1.outlet_pressure == s2.pressure
    assert eq1.outlet_mass_flowrate == s2.mass_flowrate
    
   