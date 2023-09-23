import pytest
import unittest
from propylean.instruments.measurement import TemperatureGuage
from propylean.streams import MaterialStream, EnergyStream
import propylean.properties as prop

class test_TemperatureGuage(unittest.TestCase):
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_TemperatureGuage_instantiation_only_tag(self):
        temp_guage = TemperatureGuage(tag="TT-101")
        self.assertEqual(temp_guage.tag, "TT-101")
        self.assertEqual(temp_guage.measured_unit, "C")
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_TemperatureGuage_instantiation_tag_and_measured_unit(self):
        temp_guage = TemperatureGuage(tag="TT_2",
                          measured_unit="F")
        self.assertEqual(temp_guage.tag, "TT_2")
        self.assertEqual(temp_guage.measured_unit, "F")
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_TemperatureGuage_instantiation_no_arguments(self):
        tt = TemperatureGuage()
        self.assertIsNotNone(tt.tag)
    
    @pytest.mark.positive
    def test_TemperatureGuage_representation(self):
        tt = TemperatureGuage(tag="tt_5")
        self.assertIn("TemperatureGuage with tag: tt_5", str(tt))
    
    @pytest.mark.positive
    def test_TemperatureGuage_setting_i_range(self):
        tt = TemperatureGuage(tag="tt_6",
                              i_range=(1, 10))
        self.assertEqual(tt.i_range, (1, 10))
    
    @pytest.mark.positive
    def test_TemperatureGuage_setting_resolution(self):
        tt = TemperatureGuage(tag="flow_meter_7", resolution=1)
        self.assertEqual(tt.resolution, 1)
    
    @pytest.mark.positive
    def test_TemperatureGuage_setting_inlet_temperature(self):
        flow_meter = TemperatureGuage(tag="flow_meter_8",
                          pressure_drop=(0.1, 'bar'))
        flow_meter.inlet_temperature = (50, 'C')
        self.assertEqual(flow_meter.inlet_temperature, prop.Temperature(50, 'C'))
        self.assertEqual(flow_meter.outlet_temperature, prop.Temperature(50, 'C'))
    
    @pytest.mark.positive
    def test_TemperatureGuage_setting_outlet_temperature(self):
        flow_meter = TemperatureGuage(tag="flow_meter_9",
                          pressure_drop=(0.1, 'bar'))
        flow_meter.outlet_temperature = (130, 'F')
        self.assertLess(abs(flow_meter.inlet_temperature.value-130), 0.0001)
        self.assertEqual(flow_meter.inlet_temperature.unit, 'F')
        self.assertLess(abs(flow_meter.outlet_temperature.value-130), 0.0001)
        self.assertEqual(flow_meter.outlet_temperature.unit, 'F')
    
    @pytest.mark.positive
    def test_TemperatureGuage_setting_inlet_mass_flowrate(self):
        flow_meter = TemperatureGuage(tag="flow_meter_10",
                          pressure_drop=(0.1, 'bar'))
        flow_meter.inlet_mass_flowrate = (1000, 'kg/h')
        self.assertEqual(flow_meter.inlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
        self.assertEqual(flow_meter.outlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
    
    @pytest.mark.positive
    def test_TemperatureGuage_setting_outlet_mass_flowrate(self):
        flow_meter = TemperatureGuage(tag="flow_meter_11",
                          pressure_drop=(0.10, 'bar'))
        flow_meter.outlet_mass_flowrate = (1000, 'kg/h')
        self.assertEqual(flow_meter.inlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
        self.assertEqual(flow_meter.outlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
    
    @pytest.mark.positive
    def test_TemperatureGuage_connection_with_material_stream_inlet_stream_governed(self):
        flow_meter = TemperatureGuage(tag="flow_meter_12",
                          pressure_drop=(0.1, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_flow_meter_12",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(130, 'F'))
        # Test connection is made.
        self.assertTrue(flow_meter.connect_stream(inlet_stream, 'in', stream_governed=True))
        # Test inlet properties of flow_meter are equal to inlet stream's.
        self.assertEqual(flow_meter.inlet_pressure, inlet_stream.pressure)
        self.assertAlmostEqual(flow_meter.inlet_temperature.value, inlet_stream.temperature.value, 3)
        self.assertEqual(flow_meter.inlet_temperature.unit, inlet_stream.temperature.unit)
        self.assertEqual(flow_meter.inlet_mass_flowrate, inlet_stream.mass_flowrate)
        # Test outlet properties are calculated accordingly.
        self.assertEqual(flow_meter.outlet_pressure, flow_meter.inlet_pressure - flow_meter.pressure_drop)
        self.assertLess(abs(flow_meter.inlet_temperature.value - flow_meter.outlet_temperature.value), 0.001)
        self.assertEqual(flow_meter.inlet_temperature.unit, flow_meter.outlet_temperature.unit)
        self.assertEqual(flow_meter.inlet_mass_flowrate, flow_meter.outlet_mass_flowrate)

    @pytest.mark.positive
    def test_TemperatureGuage_connection_with_material_stream_outlet_stream_governed(self):
        flow_meter = TemperatureGuage(tag="flow_meter_13",
                          pressure_drop=(0.1, 'bar'))
        outlet_stream = MaterialStream(tag="Outlet_flow_meter_13",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(130, 'F'))
        # Test connection is made.
        self.assertTrue(flow_meter.connect_stream(outlet_stream, 'out', stream_governed=True))
        # Test outlet properties of flow_meter are equal to outlet stream's.
        self.assertEqual(flow_meter.outlet_pressure, outlet_stream.pressure)
        self.assertAlmostEqual(flow_meter.outlet_temperature.value, outlet_stream.temperature.value, 3)
        self.assertEqual(flow_meter.outlet_temperature.unit, outlet_stream.temperature.unit)
        self.assertEqual(flow_meter.outlet_mass_flowrate, outlet_stream.mass_flowrate)
        # Test intlet properties are calculated accordingly.
        self.assertEqual(flow_meter.inlet_pressure, flow_meter.outlet_pressure + flow_meter.pressure_drop)
        self.assertLess(abs(flow_meter.inlet_temperature.value-flow_meter.outlet_temperature.value),0.0001)
        self.assertEqual(flow_meter.inlet_mass_flowrate, flow_meter.outlet_mass_flowrate)

    @pytest.mark.positive
    def test_TemperatureGuage_connection_with_material_stream_inlet_equipment_governed(self):
        flow_meter = TemperatureGuage(tag="flow_meter_14",
                          pressure_drop=(0.1, 'bar'))

        flow_meter.inlet_pressure = (30, 'bar')
        flow_meter.inlet_mass_flowrate = (1000, 'kg/h')
        flow_meter.inlet_temperature = (320, 'K')
        inlet_stream = MaterialStream(tag="Inlet_flow_meter_14")
        # Test connection is made.
        self.assertTrue(flow_meter.connect_stream(inlet_stream, 'in', stream_governed=False))
        # Test inlet properties of flow_meter are equal to inlet stream's.
        self.assertEqual(flow_meter.inlet_pressure, inlet_stream.pressure)
        self.assertEqual(flow_meter.inlet_temperature, inlet_stream.temperature)
        self.assertEqual(flow_meter.inlet_mass_flowrate, inlet_stream.mass_flowrate)
        # Test outlet properties are calculated accordingly.
        self.assertEqual(flow_meter.outlet_pressure, flow_meter.inlet_pressure - flow_meter.pressure_drop)
        self.assertEqual(flow_meter.inlet_temperature, flow_meter.outlet_temperature)
        self.assertEqual(flow_meter.inlet_mass_flowrate, flow_meter.outlet_mass_flowrate)

    @pytest.mark.positive
    def test_TemperatureGuage_connection_with_material_stream_outlet_equipment_governed(self):
        flow_meter = TemperatureGuage(tag="flow_meter_15",
                          pressure_drop=(0.1, 'bar'))
        flow_meter.outlet_pressure = (130, 'bar')
        flow_meter.outlet_mass_flowrate = (1000, 'kg/h')
        flow_meter.outlet_temperature = (30, 'C')
        outlet_stream = MaterialStream(tag="Outlet_flow_meter_15")
        # Test connection is made.
        self.assertTrue(flow_meter.connect_stream(outlet_stream, 'out', stream_governed=False))
        # Test outlet properties of flow_meter are equal to outlet stream's.
        self.assertEqual(flow_meter.outlet_pressure, outlet_stream.pressure)
        self.assertEqual(flow_meter.outlet_temperature, outlet_stream.temperature)
        self.assertEqual(flow_meter.outlet_mass_flowrate, outlet_stream.mass_flowrate)
        # Test intlet properties are calculated accordingly.
        self.assertEqual(flow_meter.inlet_pressure, flow_meter.outlet_pressure + flow_meter.pressure_drop)
        self.assertEqual(flow_meter.inlet_temperature, flow_meter.outlet_temperature)
        self.assertEqual(flow_meter.inlet_mass_flowrate, flow_meter.outlet_mass_flowrate)

    # pytest.mark.positive
    # def test_TemperatureGuage_connection_with_energy_stream_inlet_equipment_governed(self):
    #     flow_meter = TemperatureGuage(tag="flow_meter_17",
    #                       pressure_drop=(0.1, 'bar'))
    #     flow_meter_energy_expelled = EnergyStream(tag="Power_flow_meter_17", amount=(10,"MW"))
    #     flow_meter_inlet = MaterialStream(mass_flowrate=(1000, 'kg/h'),
    #                                 pressure=(30, 'bar'),
    #                                 temperature=(25, 'C'))
    #     flow_meter_inlet.components = prop.Components({"water": 1})
    #     # Test connection is made.
    #     self.assertTrue(flow_meter.connect_stream(flow_meter_inlet, "in", stream_governed=True))
    #     # Test inlet properties of flow_meter are equal to outlet stream's.
    #     self.assertAlmostEqual(flow_meter.energy_out.value, flow_meter_energy_expelled.amount.value)
    #     self.assertEqual(flow_meter.energy_out.unit, flow_meter_energy_expelled.amount.unit)
    
    @pytest.mark.positive
    def test_TemperatureGuage_stream_disconnection_by_stream_object(self):
        flow_meter = TemperatureGuage(tag="flow_meter_18",
                          pressure_drop=(0.1, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_flow_meter_18", pressure=(20, 'bar'))
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream(tag="Outlet_flow_meter_18")
        # Test connection is made.
        self.assertTrue(flow_meter.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(flow_meter.connect_stream(outlet_stream, 'out', stream_governed=False))
        # Test disconnection
        self.assertTrue(flow_meter.disconnect_stream(inlet_stream))
        self.assertTrue(flow_meter.disconnect_stream(outlet_stream))
        self.assertIsNone(flow_meter._inlet_material_stream_tag)
        self.assertIsNone(flow_meter._outlet_material_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)
    
    @pytest.mark.positive
    @pytest.mark.temp
    def test_TemperatureGuage_stream_disconnection_by_stream_tag(self):
        flow_meter = TemperatureGuage(tag="flow_meter_19",
                          pressure_drop=(0.1, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_flow_meter_19")
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream(tag="Outlet_flow_meter_19", pressure=(20, 'bar'))
        # Test connection is made.
        self.assertTrue(flow_meter.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(flow_meter.connect_stream(outlet_stream, 'out', stream_governed=False))
        self.assertEqual(inlet_stream.components, outlet_stream.components)
        # Test disconnection
        self.assertTrue(flow_meter.disconnect_stream(stream_tag="Inlet_flow_meter_19"))
        self.assertTrue(flow_meter.disconnect_stream(stream_tag="Outlet_flow_meter_19"))
        self.assertIsNone(flow_meter._inlet_material_stream_tag)
        self.assertIsNone(flow_meter._outlet_material_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)
    
    @pytest.mark.positive
    def test_TemperatureGuage_stream_disconnection_by_direction_stream_type(self):
        flow_meter = TemperatureGuage(tag="TT_20",
                          pressure_drop=(0.1, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_TT_20", pressure=(20, 'bar'))
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream(tag="Outlet_TT_20")
        flow_meter_energy_expelled = EnergyStream(tag="Power_TT_20")
        # Test connection is made.
        self.assertTrue(flow_meter.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(flow_meter.connect_stream(outlet_stream, 'out', stream_governed=False))
        
        # Test disconnection
        self.assertTrue(flow_meter.disconnect_stream(direction="in", stream_type="Material"))
        self.assertTrue(flow_meter.disconnect_stream(direction="ouTlet", stream_type="materiaL"))
        self.assertIsNone(flow_meter._inlet_material_stream_tag)
        self.assertIsNone(flow_meter._outlet_material_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)

    @pytest.mark.negative
    def test_TemperatureGuage_inlet_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = TemperatureGuage()
            m4.inlet_pressure = []
        self.assertIn("Incorrect type 'list' provided to 'inlet_pressure'. Should be '('Pressure', 'int', 'float', 'tuple')'",
                      str(exp))

    @pytest.mark.negative
    def test_TemperatureGuage_outlet_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = TemperatureGuage()
            m4.outlet_pressure = []
        self.assertIn("Incorrect type 'list' provided to 'outlet_pressure'. Should be '('Pressure', 'int', 'float', 'tuple')'",
                      str(exp)) 

    @pytest.mark.negative
    def test_TemperatureGuage_pressure_drop_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = TemperatureGuage()
            m4.pressure_drop = []
        self.assertIn("Incorrect type 'list' provided to 'pressure_drop'. Should be '('Pressure', 'int', 'float', 'tuple')'",
                      str(exp))                                    

    @pytest.mark.negative
    def test_TemperatureGuage_design_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = TemperatureGuage()
            m4.design_pressure = []
        self.assertIn("Incorrect type 'list' provided to 'design_pressure'. Should be '('Pressure', 'int', 'float', 'tuple')'",
                      str(exp)) 

    @pytest.mark.negative
    def test_TemperatureGuage_inlet_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = TemperatureGuage()
            m4.inlet_temperature = []
        self.assertIn("Incorrect type 'list' provided to 'inlet_temperature'. Should be '('Temperature', 'int', 'float', 'tuple')'",
                      str(exp))

    @pytest.mark.negative
    def test_TemperatureGuage_outlet_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = TemperatureGuage()
            m4.outlet_temperature = []
        self.assertIn("Incorrect type 'list' provided to 'outlet_temperature'. Should be '('Temperature', 'int', 'float', 'tuple')'",
                      str(exp)) 

    @pytest.mark.negative
    def test_TemperatureGuage_temperature_decrease_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = TemperatureGuage()
            m4.temperature_decrease = []
        self.assertIn("Incorrect type 'list' provided to 'temperature_decrease'. Should be '('Temperature', 'int', 'float', 'tuple')'",
                      str(exp)) 

    @pytest.mark.negative
    def test_TemperatureGuage_temperature_increase_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = TemperatureGuage()
            m4.temperature_increase = []
        self.assertIn("Incorrect type 'list' provided to 'temperature_increase'. Should be '('Temperature', 'int', 'float', 'tuple')'",
                      str(exp))                                                      

    @pytest.mark.negative
    def test_TemperatureGuage_design_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = TemperatureGuage()
            m4.design_temperature = []
        self.assertIn("Incorrect type 'list' provided to 'design_temperature'. Should be '('Temperature', 'int', 'float', 'tuple')'",
                      str(exp)) 

    @pytest.mark.negative
    def test_TemperatureGuage_inlet_mass_flowrate_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = TemperatureGuage()
            m4.inlet_mass_flowrate = []
        self.assertIn("Incorrect type 'list' provided to 'inlet_mass_flowrate'. Should be '('MassFlowRate', 'int', 'float', 'tuple')'",
                      str(exp))                   

    @pytest.mark.negative
    def test_TemperatureGuage_outlet_mass_flowrate_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = TemperatureGuage()
            m4.outlet_mass_flowrate = []
        self.assertIn("Incorrect type 'list' provided to 'outlet_mass_flowrate'. Should be '('MassFlowRate', 'int', 'float', 'tuple')'",
                      str(exp))

    @pytest.mark.negative
    def test_TemperatureGuage_energy_in_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = TemperatureGuage()
            m4.energy_in = []
        self.assertIn("Incorrect type 'list' provided to 'energy_in'. Should be '('Power', 'int', 'float', 'tuple')'",
                      str(exp))      

    @pytest.mark.negative
    def test_TemperatureGuage_energy_out_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = TemperatureGuage()
            m4.energy_out = []
        self.assertIn("Incorrect type 'list' provided to 'energy_out'. Should be '('Power', 'int', 'float', 'tuple')'",
                      str(exp))        

    @pytest.mark.negative
    def test_TemperatureGuage_stream_connecion_disconnection_incorrect_type(self):
        cv = TemperatureGuage()
        inlet_stream = MaterialStream(pressure=(20, 'bar'))
        inlet_stream.components = prop.Components({"water": 1})
            
        with pytest.raises(Exception) as exp:
            cv.connect_stream([inlet_stream], 'in', stream_governed=True)
        self.assertIn("Incorrect type \'list\' provided to \'stream_object\'. Should be \'('MaterialStream', 'EnergyStream')\'",
                      str(exp)) 
        
        with pytest.raises(Exception) as exp:
            cv.connect_stream(inlet_stream, ['in'], stream_governed=True)
        self.assertIn("Incorrect type \'list\' provided to \'direction\'. Should be \'str\'",
                      str(exp)) 
        with pytest.raises(Exception) as exp:
            cv.connect_stream(inlet_stream, 'in', stream_governed=[True])
        self.assertIn("Incorrect type \'list\' provided to \'stream_governed\'. Should be \'bool\'",
                      str(exp)) 

        cv.connect_stream(inlet_stream, 'in', stream_governed=True)
        with pytest.raises(Exception) as exp:
            cv.disconnect_stream(stream_tag=["Inlet_cv_19"])
        self.assertIn("Incorrect type \'list\' provided to \'stream_tag\'. Should be \'str\'",
                      str(exp))    

    @pytest.mark.negative
    def test_TemperatureGuage_stream_disconnection_before_connecion(self):  
        cv = TemperatureGuage()
        inlet_stream = MaterialStream(pressure=(20, 'bar'))
        inlet_stream.components = prop.Components({"water": 1})
        import warnings
        with warnings.catch_warnings(record=True) as exp:
            cv.disconnect_stream(inlet_stream)
         
        self.assertIn("Already there is no connection.",
                      str(exp[-1].message))    
    
    @pytest.mark.mapping
    def test_TemperatureGuage_stream_equipment_mapping(self):
        from propylean.equipments.abstract_equipment_classes import _material_stream_equipment_map as mse_map
        from propylean.equipments.abstract_equipment_classes import _energy_stream_equipment_map as ese_map
        flow_meter = TemperatureGuage(pressure_drop=(0.1, 'bar'))
        inlet_stream = MaterialStream(pressure=(20, 'bar'))
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream()

        flow_meter.connect_stream(inlet_stream, direction="in")
        flow_meter.connect_stream(outlet_stream, direction="out")

        self.assertEqual(mse_map[inlet_stream.index][2], flow_meter.index)
        self.assertEqual(mse_map[inlet_stream.index][3], flow_meter.__class__)
        self.assertEqual(mse_map[outlet_stream.index][0], flow_meter.index)
        self.assertEqual(mse_map[outlet_stream.index][1], flow_meter.__class__)    

        flow_meter.disconnect_stream(inlet_stream)
        flow_meter.disconnect_stream(outlet_stream) 

        self.assertIsNone(mse_map[inlet_stream.index][2])
        self.assertIsNone(mse_map[inlet_stream.index][3])
        self.assertIsNone(mse_map[outlet_stream.index][0])
        self.assertIsNone(mse_map[outlet_stream.index][1]) 


    @pytest.mark.delete 
    def test_TemperatureGuage_stream_equipment_delete_without_connection(self):
        flow_meter = TemperatureGuage(pressure_drop=(0.1, 'bar'))   
        print(flow_meter)
        flow_meter.delete()
        with pytest.raises(Exception) as exp:
            print(flow_meter)        
                      