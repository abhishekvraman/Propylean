import pytest
import unittest
from propylean.equipments.static import PipeSegment
from propylean.streams import MaterialStream, EnergyStream
import propylean.properties as prop
import pandas as pd
from unittest.mock import patch

class test_PipeSegment(unittest.TestCase):

    @pytest.mark.positive
    def test_PipeSegment_representation(self):
        ps = PipeSegment(tag="Pipe_1", ID=(20, "cm"), length=10)
        self.assertIn("Pipe Segment with tag: Pipe_1", str(ps))

    @pytest.mark.positive
    def test_PipeSegment_required_arguments_OD(self):
        ps = PipeSegment(ID=(20, "cm"), 
                         OD=prop.Length(220, "mm"),
                         length=10)
        self.assertEqual(ps.ID, prop.Length(20, "cm"))
        self.assertEqual(ps.OD, prop.Length(220, "mm"))
        self.assertEqual(ps.thickness, prop.Length(20, "mm"))
        self.assertEqual(ps.length, prop.Length(10, "m"))
    
    @pytest.mark.positive
    def test_PipeSegment_required_arguments_ID_and_thickness(self):
        ps = PipeSegment(ID=(20, "cm"), 
                         thickness=prop.Length(20, "mm"),
                         length=10)
        self.assertEqual(ps.ID, prop.Length(20, "cm"))
        self.assertEqual(ps.OD, prop.Length(220, "mm"))
        self.assertEqual(ps.thickness, prop.Length(20, "mm"))
        self.assertEqual(ps.length, prop.Length(10, "m"))
    
    @pytest.mark.positive
    def test_PipeSegment_required_arguments_OD_and_thickness(self):
        ps = PipeSegment(OD=(22, "cm"), 
                         thickness=prop.Length(20, "mm"),
                         length=10)
        self.assertEqual(ps.ID, prop.Length(20, "cm"))
        self.assertEqual(ps.OD, prop.Length(220, "mm"))
        self.assertEqual(ps.thickness, prop.Length(20, "mm"))
        self.assertEqual(ps.length, prop.Length(10, "m"))
    
    @pytest.mark.positive
    def test_PipeSegment_all_arguments_except_segment_frame(self):
        ps = PipeSegment(ID=(18,"cm"),
                         OD=(22, "cm"), 
                         thickness=prop.Length(20, "mm"),
                         segment_type=1,
                         material=1,
                         length=10,
                         elevation=1)
        self.assertEqual(ps.ID, prop.Length(18, "cm"))
        self.assertEqual(ps.OD, prop.Length(220, "mm"))
        self.assertEqual(ps.thickness, prop.Length(40, "mm"))
        self.assertEqual(ps.length, prop.Length(10, "m"))
        self.assertEqual(ps.elevation, prop.Length(1, "m"))
    
    @pytest.mark.positive
    def test_PipeSegment_segment_type(self):
        for i in range(1, 12):
            ps = PipeSegment(ID=(20, "cm"), 
                            segment_type=i,
                            length=10)
            self.assertEqual(ps.segment_type, i)
    
    @pytest.mark.positive
    def test_PipeSegment_material_type(self):
        for i in range(1, 5):
            ps = PipeSegment(ID=(20, "cm"), 
                            material=i,
                            length=10)
            self.assertEqual(ps.material, i)
    
    @pytest.mark.positive
    def test_PipeSegment_setting_inlet_pressure(self):
        ps = PipeSegment(ID=(20, "cm"), length=10)
        ps.inlet_pressure = (30, 'bar')
        self.assertEqual(ps.inlet_pressure, prop.Pressure(30, 'bar'))

    @pytest.mark.positive
    def test_PipeSegment_setting_pressure_drop_outlet_pressure(self):
        ps = PipeSegment(ID=(20, "cm"), length=10)
        ps.inlet_pressure = (30, 'bar')
        self.assertEqual(ps.inlet_pressure, prop.Pressure(30, 'bar'))
        self.assertEqual(ps.outlet_pressure, prop.Pressure(30, 'bar'))
        self.assertEqual(ps.pressure_drop, prop.Pressure(0, 'bar'))
    
    @pytest.mark.positive
    def test_PipeSegment_setting_outlet_pressure(self):
        ps = PipeSegment(ID=(20, "cm"), length=10)
        ps.outlet_pressure = (130, 'bar')
        self.assertEqual(ps.inlet_pressure, prop.Pressure(130, 'bar'))
        self.assertEqual(ps.outlet_pressure, prop.Pressure(130, 'bar'))
    
    @pytest.mark.positive
    def test_PipeSegment_setting_inlet_temperature(self):
        ps = PipeSegment(ID=(20, "cm"), length=10)
        ps.inlet_temperature = (50, 'C')
        self.assertEqual(ps.inlet_temperature, prop.Temperature(50, 'C'))
        self.assertEqual(ps.outlet_temperature, prop.Temperature(50, 'C'))
    
    @pytest.mark.positive
    def test_PipeSegment_setting_outlet_temperature(self):
        ps = PipeSegment(ID=(20, "cm"), length=10)
        ps.outlet_temperature = (130, 'F')
        self.assertLess(abs(ps.inlet_temperature.value-130), 0.0001)
        self.assertEqual(ps.inlet_temperature.unit, 'F')
        self.assertLess(abs(ps.outlet_temperature.value-130), 0.0001)
        self.assertEqual(ps.outlet_temperature.unit, 'F')
    
    @pytest.mark.positive
    def test_PipeSegment_setting_inlet_mass_flowrate(self):
        ps = PipeSegment(ID=(20, "cm"), length=10)
        ps.inlet_mass_flowrate = (1000, 'kg/h')
        self.assertEqual(ps.inlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
        self.assertEqual(ps.outlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
    
    @pytest.mark.positive
    def test_PipeSegment_setting_outlet_mass_flowrate(self):
        ps = PipeSegment(ID=(20, "cm"), length=10)
        ps.outlet_mass_flowrate = (1000, 'kg/h')
        self.assertEqual(ps.inlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
        self.assertEqual(ps.outlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
    
    @pytest.mark.positive
    def test_PipeSegment_connection_with_material_stream_inlet_stream_governed(self):
        ps = PipeSegment(ID=(20, "cm"), length=10)
        inlet_stream = MaterialStream(tag="Inlet_ps_12",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(130, 'F'))
        inlet_stream.components = prop.Components({"water": 1})
        # Test connection is made.
        self.assertTrue(ps.connect_stream(inlet_stream, 'in', stream_governed=True))
        # Test inlet properties of ps are equal to inlet stream's.
        self.assertEqual(ps.inlet_pressure, inlet_stream.pressure)
        self.assertEqual(ps.inlet_temperature, inlet_stream.temperature)
        self.assertEqual(ps.inlet_mass_flowrate, inlet_stream.mass_flowrate)
        # Test outlet properties are calculated accordingly.
        self.assertEqual(ps.outlet_pressure, ps.inlet_pressure-ps.pressure_drop)
        self.assertLess(abs(ps.inlet_temperature.value - ps.outlet_temperature.value), 0.001)
        self.assertEqual(ps.inlet_temperature.unit, ps.outlet_temperature.unit)
        self.assertEqual(ps.inlet_mass_flowrate, ps.outlet_mass_flowrate)

    @pytest.mark.positive
    def test_PipeSegment_connection_with_material_stream_outlet_stream_governed(self):
        ps = PipeSegment(ID=(20, "cm"), length=10)
        outlet_stream = MaterialStream(tag="Outlet_ps_13",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(130, 'F'))
        outlet_stream.components = prop.Components({"water": 1})
        # Test connection is made.
        self.assertTrue(ps.connect_stream(outlet_stream, 'out', stream_governed=True))
        # Test outlet properties of ps are equal to outlet stream's.
        self.assertEqual(ps.outlet_pressure, outlet_stream.pressure)
        self.assertEqual(ps.outlet_temperature, outlet_stream.temperature)
        self.assertEqual(ps.outlet_mass_flowrate, outlet_stream.mass_flowrate)
        # Test intlet properties are calculated accordingly.
        self.assertEqual(ps.inlet_pressure, ps.outlet_pressure+ps.pressure_drop)
        self.assertLess(abs(ps.inlet_temperature.value-ps.outlet_temperature.value),0.0001)
        self.assertEqual(ps.inlet_mass_flowrate, ps.outlet_mass_flowrate)

    @pytest.mark.positive
    def test_PipeSegment_connection_with_material_stream_inlet_equipment_governed(self):
        ps = PipeSegment(ID=(20, "cm"), length=10)
        ps.inlet_pressure = (30, 'bar')
        ps.inlet_mass_flowrate = (1000, 'kg/h')
        ps.inlet_temperature = (320, 'K')
        inlet_stream = MaterialStream(tag="Inlet_ps_14")
        inlet_stream.components = prop.Components({"water": 1})
        # Test connection is made.
        self.assertTrue(ps.connect_stream(inlet_stream, 'in', stream_governed=False))
        # Test inlet properties of ps are equal to inlet stream's.
        self.assertEqual(ps.inlet_pressure, inlet_stream.pressure)
        self.assertEqual(ps.inlet_temperature, inlet_stream.temperature)
        self.assertEqual(ps.inlet_mass_flowrate, inlet_stream.mass_flowrate)
        # Test outlet properties are calculated accordingly.
        self.assertEqual(ps.outlet_pressure, ps.inlet_pressure-ps.pressure_drop)
        self.assertEqual(ps.inlet_temperature, ps.outlet_temperature)
        self.assertEqual(ps.inlet_mass_flowrate, ps.outlet_mass_flowrate)

    @pytest.mark.positive
    def test_PipeSegment_connection_with_material_stream_outlet_equipment_governed(self):
        ps = PipeSegment(ID=(20, "cm"), length=10)
        ps.outlet_pressure = (130, 'bar')
        ps.outlet_mass_flowrate = (1000, 'kg/h')
        ps.outlet_temperature = (30, 'C')
        outlet_stream = MaterialStream(tag="Outlet_ps_15")
        outlet_stream.components = prop.Components({"water": 1})
        # Test connection is made.
        self.assertTrue(ps.connect_stream(outlet_stream, 'out', stream_governed=False))
        # Test outlet properties of ps are equal to outlet stream's.
        self.assertEqual(ps.outlet_pressure, outlet_stream.pressure)
        self.assertEqual(ps.outlet_temperature, outlet_stream.temperature)
        self.assertEqual(ps.outlet_mass_flowrate, outlet_stream.mass_flowrate)
        # Test intlet properties are calculated accordingly.
        self.assertEqual(ps.inlet_pressure, ps.outlet_pressure+ps.pressure_drop)
        self.assertEqual(ps.inlet_temperature, ps.outlet_temperature)
        self.assertEqual(ps.inlet_mass_flowrate, ps.outlet_mass_flowrate)
    
    # TODO Uncomment below when power setting feature is provided.
    # @pytest.mark.positive
    # def test_PipeSegment_connection_with_energy_stream_inlet_stream_governed(self):
    #     ps = PipeSegment(ID=(20, "cm"), length=10)
    #     ps_power = EnergyStream(tag="Power_ps_16", amount=(10,"MW"))
    #     # Test connection is made.
    #     self.assertTrue(ps.connect_stream(ps_power, stream_governed=True))
    #     # Test inlet properties of ps are equal to outlet stream's.
    #     self.assertEqual(ps.energy_in, ps_power.amount)

    pytest.mark.positive
    def test_PipeSegment_connection_with_energy_stream_inlet_equipment_governed(self):
        ps = PipeSegment(ID=(20, "cm"), length=10)
        ps_power = EnergyStream(tag="Power_ps_17", amount=(10,"MW"))
        ps_inlet = MaterialStream(mass_flowrate=(1000, 'kg/h'),
                                    pressure=(30, 'bar'),
                                    temperature=(25, 'C'))
        ps_inlet.components = prop.Components({"water": 1})
        # Test connection is made.
        self.assertTrue(ps.connect_stream(ps_inlet, "in", stream_governed=True))
        self.assertTrue(ps.connect_stream(ps_power, "in"))
        # Test inlet properties of ps are equal to outlet stream's.
        self.assertAlmostEqual(ps.energy_in.value, ps_power.amount.value)
        self.assertEqual(ps.energy_in.unit, ps_power.amount.unit)
    
    @pytest.mark.positive
    def test_PipeSegment_stream_disconnection_by_stream_object(self):
        ps = PipeSegment(ID=(20, "cm"), length=10)
        inlet_stream = MaterialStream(tag="Inlet_ps_18")
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream(tag="Outlet_ps_18")
        ps_power = EnergyStream(tag="Power_ps_18")
        # Test connection is made.
        self.assertTrue(ps.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(ps.connect_stream(outlet_stream, 'out', stream_governed=False))
        self.assertTrue(ps.connect_stream(ps_power, "out"))
        # Test disconnection
        self.assertTrue(ps.disconnect_stream(inlet_stream))
        self.assertTrue(ps.disconnect_stream(outlet_stream))
        self.assertTrue(ps.disconnect_stream(ps_power))
        self.assertIsNone(ps._inlet_material_stream_tag)
        self.assertIsNone(ps._outlet_material_stream_tag)
        self.assertIsNone(ps._inlet_energy_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)
    
    @pytest.mark.positive
    @pytest.mark.temp
    def test_PipeSegment_stream_disconnection_by_stream_tag(self):
        ps = PipeSegment(ID=(20, "cm"), length=10)
        inlet_stream = MaterialStream(tag="Inlet_ps_19")
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream(tag="Outlet_ps_19")
        ps_power = EnergyStream(tag="Power_ps_19")
        # Test connection is made.
        self.assertTrue(ps.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(ps.connect_stream(outlet_stream, 'out', stream_governed=False))
        self.assertEqual(inlet_stream.components, outlet_stream.components)
        self.assertTrue(ps.connect_stream(ps_power, "in"))
        # Test disconnection
        self.assertTrue(ps.disconnect_stream(stream_tag="Inlet_ps_19"))
        self.assertTrue(ps.disconnect_stream(stream_tag="Outlet_ps_19"))
        self.assertTrue(ps.disconnect_stream(stream_tag="Power_ps_19"))
        self.assertIsNone(ps._inlet_material_stream_tag)
        self.assertIsNone(ps._outlet_material_stream_tag)
        self.assertIsNone(ps._inlet_energy_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)
    
    @pytest.mark.positive
    def test_PipeSegment_stream_disconnection_by_direction_stream_type(self):
        ps = PipeSegment(ID=(20, "cm"), length=10)
        inlet_stream = MaterialStream(tag="Inlet_ps_20")
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream(tag="Outlet_ps_20")
        ps_power = EnergyStream(tag="Power_ps_20")
        # Test connection is made.
        self.assertTrue(ps.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(ps.connect_stream(outlet_stream, 'out', stream_governed=False))
        self.assertTrue(ps.connect_stream(ps_power, "out"))
        # Test disconnection
        self.assertTrue(ps.disconnect_stream(direction="In", stream_type="Material"))
        self.assertTrue(ps.disconnect_stream(direction="ouTlet", stream_type="materiaL"))
        self.assertTrue(ps.disconnect_stream(stream_type="energy", direction="out"))
        self.assertIsNone(ps._inlet_material_stream_tag)
        self.assertIsNone(ps._outlet_material_stream_tag)
        self.assertIsNone(ps._inlet_energy_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)

    @pytest.mark.positive
    def test_PipeSegment_pressure_drop_friction_straight_pipe_liquid(self):
        ps = PipeSegment(ID=(347.675, "mm"), length=(10, 'm'))
        inlet_stream = MaterialStream(mass_flowrate=(100000, 'kg/min'),
                                      pressure=(100, 'bar'),
                                      temperature=(40, 'C'))
        inlet_stream.components = prop.Components({"water": 1})
        ps.connect_stream(inlet_stream, 'in', stream_governed=True)
        ps.pressure_drop.unit = "bar"
        from propylean.settings import Settings
        Settings.pipe_dp_method = "Colebrook"
        # TODO Change assert for better accuracy of pressure drop calculations
        self.assertGreater(ps.pressure_drop.value, 0)
    
    @pytest.mark.positive
    def test_PipeSegment_pressure_drop_straight_pipe_elevated_liquid(self):
        ps = PipeSegment(ID=(347.675, "mm"), length=(20, 'm'), elevation=(10, 'm'))
        inlet_stream = MaterialStream(mass_flowrate=(100000, 'kg/min'),
                                      pressure=(100, 'bar'),
                                      temperature=(40, 'C'))
        inlet_stream.components = prop.Components({"water": 1})
        ps.connect_stream(inlet_stream, 'in', stream_governed=True)
        ps.pressure_drop.unit = "bar"
        hydrostatic_pressure = ps.dp_hydrostatic(prop.Density(995.621))
        hydrostatic_pressure.unit = "bar"
        self.assertAlmostEqual(hydrostatic_pressure.value, 
                               prop.Pressure(0.9576, 'bar').value, 1)
        from propylean.settings import Settings
        Settings.pipe_dp_method = "Colebrook"
        # TODO Change assert for better accuracy of pressure drop calculations
        self.assertGreater(ps.pressure_drop.value, 0)
    
    @pytest.mark.positive
    @pytest.mark.segment_frame
    def test_PipeSegment_pressure_drop_segment_frame_liquid(self):
        segment_frame = pd.DataFrame({'segment_type': [1, 2, 6, 12],
                                      'ID': [(34.7675, 'cm'), (34.7675, 'cm'), (34.7675, 'cm'), (18, 'cm')],
                                      'length': [(20, 'm'), None, None, None],
                                      'material': [2, 2, 2, 2],
                                      'elevation': [(10, 'm'), None, None, None],
                                      'shape': [None, None, None, (20, 18)]})
        ps = PipeSegment(segment_frame=segment_frame)
        inlet_stream = MaterialStream(mass_flowrate=(100000, 'kg/min'),
                                      pressure=(100, 'bar'),
                                      temperature=(40, 'C'))
        inlet_stream.components = prop.Components({"water": 1})
        self.assertTrue(ps.connect_stream(inlet_stream, 'in', stream_governed=True))
        ps.pressure_drop.unit = "bar"
        from propylean.settings import Settings
        Settings.pipe_dp_method = "Colebrook"
        # TODO Change assert for better accuracy of pressure drop calculations
        self.assertGreater(ps.pressure_drop.value, 0)
    
    @pytest.mark.positive
    def test_PipeSegment_pressure_drop_others(self):
        for i in range(2, 12):
            ps = PipeSegment(ID=(347.675, "mm"), segment_type=i)
            inlet_stream = MaterialStream(mass_flowrate=(100000, 'kg/min'),
                                          pressure=(100, 'bar'),
                                          temperature=(40, 'C'))
            inlet_stream.components = prop.Components({"water": 1})
            ps.connect_stream(inlet_stream, 'in', stream_governed=True)
            ps.pressure_drop.unit = "bar"
            
            # TODO Change assert for better accuracy of pressure drop calculations
            self.assertGreater(ps.pressure_drop.value, 0)
    
    @pytest.mark.positive
    def test_PipeSegment_pressure_drop_reducer_expander(self):
        
        ps = PipeSegment(segment_type=12, ID=(18, 'mm'), shape=(20, 18))
        inlet_stream = MaterialStream(mass_flowrate=(100000, 'kg/min'),
                                        pressure=(100, 'bar'),
                                        temperature=(40, 'C'))
        inlet_stream.components = prop.Components({"water": 1})
        ps.connect_stream(inlet_stream, 'in', stream_governed=True)
        ps.pressure_drop.unit = "bar"
        
        # TODO Change assert for better accuracy of pressure drop calculations
        self.assertGreater(ps.pressure_drop.value, 0)
        
        ps = PipeSegment(segment_type=13, ID=(18, 'mm'), shape=(20, 18))
        inlet_stream = MaterialStream(mass_flowrate=(100000, 'kg/min'),
                                        pressure=(100, 'bar'),
                                        temperature=(40, 'C'))
        inlet_stream.components = prop.Components({"water": 1})
        ps.connect_stream(inlet_stream, 'in', stream_governed=True)
        ps.pressure_drop.unit = "bar"
        
        # TODO Change assert for better accuracy of pressure drop calculations
        self.assertGreater(ps.pressure_drop.value, 0)

    @pytest.mark.negative
    def test_PipeSegment_inlet_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = PipeSegment(segment_type=13, ID=(18, 'mm'), shape=(20, 18))
            m4.inlet_pressure = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'inlet_pressure'. Should be '(<class 'propylean.properties.Pressure'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))

    @pytest.mark.negative
    def test_PipeSegment_outlet_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = PipeSegment(segment_type=13, ID=(18, 'mm'), shape=(20, 18))
            m4.outlet_pressure = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'outlet_pressure'. Should be '(<class 'propylean.properties.Pressure'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

                            
    @pytest.mark.negative
    def test_PipeSegment_design_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = PipeSegment(segment_type=13, ID=(18, 'mm'), shape=(20, 18))
            m4.design_pressure = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'design_pressure'. Should be '(<class 'propylean.properties.Pressure'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

    @pytest.mark.negative
    def test_PipeSegment_inlet_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = PipeSegment(segment_type=13, ID=(18, 'mm'), shape=(20, 18))
            m4.inlet_temperature = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'inlet_temperature'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))

    @pytest.mark.negative
    def test_PipeSegment_outlet_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = PipeSegment(segment_type=13, ID=(18, 'mm'), shape=(20, 18))
            m4.outlet_temperature = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'outlet_temperature'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

    @pytest.mark.negative
    def test_PipeSegment_temperature_decrease_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = PipeSegment(segment_type=13, ID=(18, 'mm'), shape=(20, 18))
            m4.temperature_decrease = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'temperature_decrease'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

    @pytest.mark.negative
    def test_PipeSegment_temperature_increase_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = PipeSegment(segment_type=13, ID=(18, 'mm'), shape=(20, 18))
            m4.temperature_increase = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'temperature_increase'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                                                      

    @pytest.mark.negative
    def test_PipeSegment_design_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = PipeSegment(segment_type=13, ID=(18, 'mm'), shape=(20, 18))
            m4.design_temperature = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'design_temperature'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

    @pytest.mark.negative
    def test_PipeSegment_inlet_mass_flowrate_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = PipeSegment(segment_type=13, ID=(18, 'mm'), shape=(20, 18))
            m4.inlet_mass_flowrate = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'inlet_mass_flowrate'. Should be '(<class 'propylean.properties.MassFlowRate'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                   

    @pytest.mark.negative
    def test_PipeSegment_outlet_mass_flowrate_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = PipeSegment(segment_type=13, ID=(18, 'mm'), shape=(20, 18))
            m4.outlet_mass_flowrate = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'outlet_mass_flowrate'. Should be '(<class 'propylean.properties.MassFlowRate'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))

    @pytest.mark.negative
    def test_PipeSegment_energy_in_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = PipeSegment(segment_type=13, ID=(18, 'mm'), shape=(20, 18))
            m4.energy_in = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'energy_in'. Should be '(<class 'propylean.properties.Power'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))      

    @pytest.mark.negative
    def test_PipeSegment_energy_out_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = PipeSegment(segment_type=13, ID=(18, 'mm'), shape=(20, 18))
            m4.energy_out = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'energy_out'. Should be '(<class 'propylean.properties.Power'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))

    @pytest.mark.negative
    def test_PipeSegment_length_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = PipeSegment(segment_type=13, ID=(18, 'mm'), shape=(20, 18))
            m4.length = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'length'. Should be '(<class 'propylean.properties.Length'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                  

    @pytest.mark.negative
    def test_PipeSegment_ID_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = PipeSegment(segment_type=13, ID=[18, 'mm'], shape=(20, 18))
            
        self.assertIn("Incorrect type '<class 'list'>' provided to 'ID'. Should be '(<class 'propylean.properties.Length'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                    

    @pytest.mark.negative
    def test_PipeSegment_OD_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = PipeSegment(segment_type=13, ID=(18, 'mm'), shape=(20, 18))
            m4.OD = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'OD'. Should be '(<class 'propylean.properties.Length'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                  

    @pytest.mark.negative
    def test_PipeSegment_elevation_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = PipeSegment(segment_type=13, ID=(18, 'mm'), shape=(20, 18))
            m4.elevation = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'elevation'. Should be '(<class 'propylean.properties.Length'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                   

    @pytest.mark.negative
    def test_PipeSegment_segmen_type_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = PipeSegment(segment_type=[13], ID=(18, 'mm'), shape=(20, 18))
            
        self.assertIn("Incorrect type '<class 'list'>' provided to 'segment_type'. Should be '<class 'int'>'",
                      str(exp))  
        with pytest.raises(Exception) as exp:
            m4 = PipeSegment(length=(10, "m"), ID=(18, 'mm'), shape=(20, 18))
            m4.segment_type = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'segment_type'. Should be '<class 'int'>'",
                      str(exp))                                  

    @pytest.mark.negative
    def test_PipeSegment_material_incorrect_type_to_value(self):
         
        with pytest.raises(Exception) as exp:
            m4 = PipeSegment(length=(10, "m"), ID=(18, 'mm'), shape=(20, 18))
            m4.material = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'material'. Should be '<class 'int'>'",
                      str(exp))                    