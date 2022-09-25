import pytest
import unittest
from propylean.equipments.rotary import CentrifugalPump
from propylean.streams import MaterialStream, EnergyStream
import propylean.properties as prop
import pandas as pd
from unittest.mock import patch
from propylean import MaterialStream, EnergyStream

class test_CentrifugalPump(unittest.TestCase):
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_CentrifugalPump_instantiation_only_tag(self):
        pump = CentrifugalPump(tag="Pump_1")
        self.assertEqual(pump.tag, "Pump_1")
        self.assertEqual(pump.pressure_drop, prop.Pressure(0))
        self.assertEqual(pump.differential_pressure, prop.Pressure(0))
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_CentrifugalPump_instantiation_tag_and_differential_pressure(self):
        pump = CentrifugalPump(tag="Pump_2",
                               differential_pressure=prop.Pressure(100, 'bar'))
        self.assertEqual(pump.tag, "Pump_2")
        self.assertEqual(pump.differential_pressure, prop.Pressure(100, 'bar'))
        self.assertEqual(pump.pressure_drop, prop.Pressure(-100, 'bar'))
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_CentrifugalPump_instantiation_no_arguments(self):
        pump = CentrifugalPump()
        self.assertIsNotNone(pump.tag)
        self.assertEqual(pump.pressure_drop, prop.Pressure(0))
        self.assertEqual(pump.differential_pressure, prop.Pressure(0))
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_CentrifugalPump_instantiation_min_flow_npshr_efficiency(self):
        pump = CentrifugalPump(tag="Pump_3",
                               differential_pressure=(100, 'bar'),
                               min_flow = (100, "lit/h"),
                               NPSHr=(4, 'm'),
                               efficiency=70 )
        self.assertEqual(pump.tag, "Pump_3")
        self.assertEqual(pump.differential_pressure, prop.Pressure(100, 'bar'))
        self.assertEqual(pump.min_flow, prop.VolumetricFlowRate(100, "lit/h"))
        self.assertEqual(pump.NPSHr, prop.Length(4, 'm'))
        self.assertEqual(pump.efficiency, 0.70)
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_CentrifugalPump_instantiation_pump_curves(self):
        performance_curve = pd.DataFrame([{'flow':[2,10,30,67], 'head':[45,20,10,2]}])
        pump = CentrifugalPump(tag="Pump_4",
                               performance_curve=performance_curve)
        self.assertEqual(pump.performace_curve.shape, performance_curve.shape)
    
    @pytest.mark.positive
    def test_CentrifugalPump_representation(self):
        pump = CentrifugalPump(tag="Pump_5")
        self.assertIn("Centrifugal Pump with tag: Pump_5", str(pump))
    
    @pytest.mark.positive
    def test_CentrifugalPump_setting_inlet_pressure(self):
        pump = CentrifugalPump(tag="Pump_6",
                               differential_pressure=(100, 'bar'))
        pump.inlet_pressure = (30, 'bar')
        self.assertEqual(pump.inlet_pressure, prop.Pressure(30, 'bar'))
        self.assertEqual(pump.outlet_pressure, prop.Pressure(130, 'bar'))
    
    @pytest.mark.positive
    def test_CentrifugalPump_setting_outlet_pressure(self):
        pump = CentrifugalPump(tag="Pump_7",
                               differential_pressure=(100, 'bar'))
        pump.outlet_pressure = (130, 'bar')
        self.assertEqual(pump.inlet_pressure, prop.Pressure(30, 'bar'))
        self.assertEqual(pump.outlet_pressure, prop.Pressure(130, 'bar'))
    
    @pytest.mark.positive
    def test_CentrifugalPump_setting_inlet_temperature(self):
        pump = CentrifugalPump(tag="Pump_8",
                               differential_pressure=(100, 'bar'))
        pump.inlet_temperature = (50, 'C')
        self.assertEqual(pump.inlet_temperature, prop.Temperature(50, 'C'))
        self.assertEqual(pump.outlet_temperature, prop.Temperature(50, 'C'))
    
    @pytest.mark.positive
    def test_CentrifugalPump_setting_outlet_temperature(self):
        pump = CentrifugalPump(tag="Pump_9",
                               differential_pressure=(100, 'bar'))
        pump.outlet_temperature = (130, 'F')
        self.assertLess(abs(pump.inlet_temperature.value-130), 0.0001)
        self.assertEqual(pump.inlet_temperature.unit, 'F')
        self.assertLess(abs(pump.outlet_temperature.value-130), 0.0001)
        self.assertEqual(pump.outlet_temperature.unit, 'F')
    
    @pytest.mark.positive
    def test_CentrifugalPump_setting_inlet_mass_flowrate(self):
        pump = CentrifugalPump(tag="Pump_10",
                               differential_pressure=(100, 'bar'))
        pump.inlet_mass_flowrate = (1000, 'kg/h')
        self.assertEqual(pump.inlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
        self.assertEqual(pump.outlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
    
    @pytest.mark.positive
    def test_CentrifugalPump_setting_outlet_mass_flowrate(self):
        pump = CentrifugalPump(tag="Pump_11",
                               differential_pressure=(100, 'bar'))
        pump.outlet_mass_flowrate = (1000, 'kg/h')
        self.assertEqual(pump.inlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
        self.assertEqual(pump.outlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
    
    @pytest.mark.positive
    def test_CentrifugalPump_connection_with_material_stream_inlet_stream_governed(self):
        pump = CentrifugalPump(tag="Pump_12",
                               differential_pressure=(100, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_Pump_12",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(130, 'F'))
        # Test connection is made.
        self.assertTrue(pump.connect_stream(inlet_stream, 'in', stream_governed=True))
        # Test inlet properties of pump are equal to inlet stream's.
        self.assertEqual(pump.inlet_pressure, inlet_stream.pressure)
        self.assertAlmostEqual(pump.inlet_temperature.value, inlet_stream.temperature.value, 2)
        self.assertEqual(pump.inlet_temperature.unit, inlet_stream.temperature.unit)
        self.assertEqual(pump.inlet_mass_flowrate, inlet_stream.mass_flowrate)
        # Test outlet properties are calculated accordingly.
        self.assertEqual(pump.outlet_pressure, pump.inlet_pressure+pump.differential_pressure)
        self.assertLess(abs(pump.inlet_temperature.value - pump.outlet_temperature.value), 0.001)
        self.assertEqual(pump.inlet_temperature.unit, pump.outlet_temperature.unit)
        self.assertEqual(pump.inlet_mass_flowrate, pump.outlet_mass_flowrate)

    @pytest.mark.positive
    def test_CentrifugalPump_connection_with_material_stream_outlet_stream_governed(self):
        pump = CentrifugalPump(tag="Pump_13",
                               differential_pressure=(100, 'bar'))
        outlet_stream = MaterialStream(tag="Outlet_Pump_13",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(130, 'F'))
        # Test connection is made.
        self.assertTrue(pump.connect_stream(outlet_stream, 'out', stream_governed=True))
        # Test outlet properties of pump are equal to outlet stream's.
        self.assertEqual(pump.outlet_pressure, outlet_stream.pressure)
        self.assertAlmostEqual(pump.outlet_temperature.value, outlet_stream.temperature.value, 2)
        self.assertEqual(pump.outlet_temperature.unit, outlet_stream.temperature.unit)
        self.assertEqual(pump.outlet_mass_flowrate, outlet_stream.mass_flowrate)
        # Test intlet properties are calculated accordingly.
        self.assertEqual(pump.inlet_pressure, pump.outlet_pressure-pump.differential_pressure)
        self.assertLess(abs(pump.inlet_temperature.value-pump.outlet_temperature.value),0.0001)
        self.assertEqual(pump.inlet_mass_flowrate, pump.outlet_mass_flowrate)

    @pytest.mark.positive
    def test_CentrifugalPump_connection_with_material_stream_inlet_equipment_governed(self):
        pump = CentrifugalPump(tag="Pump_14",
                               differential_pressure=(100, 'bar'))

        pump.inlet_pressure = (30, 'bar')
        pump.inlet_mass_flowrate = (1000, 'kg/h')
        pump.inlet_temperature = (320, 'K')
        inlet_stream = MaterialStream(tag="Inlet_Pump_14")
        # Test connection is made.
        self.assertTrue(pump.connect_stream(inlet_stream, 'in', stream_governed=False))
        # Test inlet properties of pump are equal to inlet stream's.
        self.assertEqual(pump.inlet_pressure, inlet_stream.pressure)
        self.assertEqual(pump.inlet_temperature, inlet_stream.temperature)
        self.assertEqual(pump.inlet_mass_flowrate, inlet_stream.mass_flowrate)
        # Test outlet properties are calculated accordingly.
        self.assertEqual(pump.outlet_pressure, pump.inlet_pressure+pump.differential_pressure)
        self.assertEqual(pump.inlet_temperature, pump.outlet_temperature)
        self.assertEqual(pump.inlet_mass_flowrate, pump.outlet_mass_flowrate)

    @pytest.mark.positive
    def test_CentrifugalPump_connection_with_material_stream_outlet_equipment_governed(self):
        pump = CentrifugalPump(tag="Pump_15",
                               differential_pressure=(100, 'bar'))
        pump.outlet_pressure = (130, 'bar')
        pump.outlet_mass_flowrate = (1000, 'kg/h')
        pump.outlet_temperature = (30, 'C')
        outlet_stream = MaterialStream(tag="Outlet_Pump_15")
        # Test connection is made.
        self.assertTrue(pump.connect_stream(outlet_stream, 'out', stream_governed=False))
        # Test outlet properties of pump are equal to outlet stream's.
        self.assertEqual(pump.outlet_pressure, outlet_stream.pressure)
        self.assertEqual(pump.outlet_temperature, outlet_stream.temperature)
        self.assertEqual(pump.outlet_mass_flowrate, outlet_stream.mass_flowrate)
        # Test intlet properties are calculated accordingly.
        self.assertEqual(pump.inlet_pressure, pump.outlet_pressure-pump.differential_pressure)
        self.assertEqual(pump.inlet_temperature, pump.outlet_temperature)
        self.assertEqual(pump.inlet_mass_flowrate, pump.outlet_mass_flowrate)
    
    # TODO Uncomment below when power setting feature is provided.
    # @pytest.mark.positive
    # def test_CentrifugalPump_connection_with_energy_stream_inlet_stream_governed(self):
    #     pump = CentrifugalPump(tag="Pump_16",
    #                            differential_pressure=(100, 'bar'))
    #     pump_power = EnergyStream(tag="Power_Pump_16", amount=(10,"MW"))
    #     # Test connection is made.
    #     self.assertTrue(pump.connect_stream(pump_power, stream_governed=True))
    #     # Test inlet properties of pump are equal to outlet stream's.
    #     self.assertEqual(pump.energy_in, pump_power.amount)
    #     self.assertEqual(pump.power, pump_power.unit)

    pytest.mark.positive
    def test_CentrifugalPump_connection_with_energy_stream_inlet_equipment_governed(self):
        pump = CentrifugalPump(tag="Pump_17",
                               differential_pressure=(100, 'bar'))
        pump_power = EnergyStream(tag="Power_Pump_17", amount=(10,"MW"))
        pump_inlet = MaterialStream(mass_flowrate=(1000, 'kg/h'),
                                    pressure=(30, 'bar'),
                                    temperature=(25, 'C'))
        pump_inlet.components = prop.Components({"water": 1})
        # Test connection is made.
        self.assertTrue(pump.connect_stream(pump_inlet, "in", stream_governed=True))
        self.assertTrue(pump.connect_stream(pump_power))
        # Test inlet properties of pump are equal to outlet stream's.
        self.assertAlmostEqual(pump.power.value, pump_power.amount.value)
        self.assertEqual(pump.power.unit, pump_power.amount.unit)
    
    @pytest.mark.positive
    def test_CentrifugalPump_stream_disconnection_by_stream_object(self):
        pump = CentrifugalPump(tag="Pump_18",
                               differential_pressure=(100, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_Pump_18")
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream(tag="Outlet_Pump_18")
        pump_power = EnergyStream(tag="Power_Pump_18")
        # Test connection is made.
        self.assertTrue(pump.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(pump.connect_stream(outlet_stream, 'out', stream_governed=False))
        self.assertTrue(pump.connect_stream(pump_power))
        # Test disconnection
        self.assertTrue(pump.disconnect_stream(inlet_stream))
        self.assertTrue(pump.disconnect_stream(outlet_stream))
        self.assertTrue(pump.disconnect_stream(pump_power))
        self.assertIsNone(pump._inlet_material_stream_tag)
        self.assertIsNone(pump._outlet_material_stream_tag)
        self.assertIsNone(pump._inlet_energy_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)
    
    @pytest.mark.positive
    @pytest.mark.temp
    def test_CentrifugalPump_stream_disconnection_by_stream_tag(self):
        pump = CentrifugalPump(tag="Pump_19",
                               differential_pressure=(100, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_Pump_19")
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream(tag="Outlet_Pump_19")
        pump_power = EnergyStream(tag="Power_Pump_19")
        # Test connection is made.
        self.assertTrue(pump.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(pump.connect_stream(outlet_stream, 'out', stream_governed=False))
        self.assertEqual(inlet_stream.components, outlet_stream.components)
        self.assertTrue(pump.connect_stream(pump_power))
        # Test disconnection
        self.assertTrue(pump.disconnect_stream(stream_tag="Inlet_Pump_19"))
        self.assertTrue(pump.disconnect_stream(stream_tag="Outlet_Pump_19"))
        self.assertTrue(pump.disconnect_stream(stream_tag="Power_Pump_19"))
        self.assertIsNone(pump._inlet_material_stream_tag)
        self.assertIsNone(pump._outlet_material_stream_tag)
        self.assertIsNone(pump._inlet_energy_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)
    
    @pytest.mark.positive
    def test_CentrifugalPump_stream_disconnection_by_direction_stream_type(self):
        pump = CentrifugalPump(tag="Pump_20",
                               differential_pressure=(100, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_Pump_20")
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream(tag="Outlet_Pump_20")
        pump_power = EnergyStream(tag="Power_Pump_20")
        # Test connection is made.
        self.assertTrue(pump.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(pump.connect_stream(outlet_stream, 'out', stream_governed=False))
        self.assertTrue(pump.connect_stream(pump_power))
        # Test disconnection
        self.assertTrue(pump.disconnect_stream(direction="in", stream_type="Material"))
        self.assertTrue(pump.disconnect_stream(direction="ouTlet", stream_type="materiaL"))
        self.assertTrue(pump.disconnect_stream(stream_type="energy"))
        self.assertIsNone(pump._inlet_material_stream_tag)
        self.assertIsNone(pump._outlet_material_stream_tag)
        self.assertIsNone(pump._inlet_energy_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)

    @pytest.mark.positive
    def test_CentrifugalPump_head_calulcation(self):
        pump = CentrifugalPump(tag="Pump_21",
                               differential_pressure=(100, 'bar'),
                               efficiency=75)
        inlet_stream = MaterialStream(tag="Inlet_Pump_21",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(25, 'C'))
        inlet_stream.components = prop.Components({"water": 1})
        pump.connect_stream(inlet_stream, 'in', stream_governed=True)
        pressure = prop.Pressure(100, 'bar')
        pressure.unit = "Pa"
        expected_head_value = 10000000 / (9.8 * inlet_stream.density.value)
        pump_head = pump.head
        pump_head.unit = "m"
        self.assertAlmostEqual(expected_head_value, pump_head.value)
    
    @pytest.mark.positive
    def test_CentrifugalPump_power_calulcations(self):
        pump = CentrifugalPump(tag="Pump_22",
                               differential_pressure=(100, 'bar'),
                               efficiency=40)
        inlet_stream = MaterialStream(tag="Inlet_Pump_22",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(25, 'C'))
        inlet_stream.components = prop.Components({"water": 1})
        pump.connect_stream(inlet_stream, 'in', stream_governed=True)
        pressure = prop.Pressure(100, 'bar')
        pressure.unit = "Pa"
        expected_hydraulic_power = prop.Power(2.78676, "W")
        expected_brake_horse_power = expected_hydraulic_power.value/pump.efficiency
        pump_hydraulic_power = pump.hydraulic_power
        pump_hydraulic_power.unit = "kW"
        pump_brake_horse_power = pump.power
        pump_brake_horse_power.unit = "kW"
        self.assertAlmostEqual(expected_hydraulic_power.value, pump_hydraulic_power.value, 1)
        self.assertAlmostEqual(expected_brake_horse_power, pump_brake_horse_power.value, 1)

    @pytest.mark.negative
    def test_CentrifugalPump_inlet_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = CentrifugalPump()
            m4.inlet_pressure = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'inlet_pressure'. Should be '(<class 'propylean.properties.Pressure'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))

    @pytest.mark.negative
    def test_CentrifugalPump_outlet_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = CentrifugalPump()
            m4.outlet_pressure = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'outlet_pressure'. Should be '(<class 'propylean.properties.Pressure'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

    @pytest.mark.negative
    def test_CentrifugalPump_pressure_drop_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = CentrifugalPump()
            m4.pressure_drop = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'pressure_drop'. Should be '(<class 'propylean.properties.Pressure'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                                    

    @pytest.mark.negative
    def test_CentrifugalPump_design_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = CentrifugalPump()
            m4.design_pressure = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'design_pressure'. Should be '(<class 'propylean.properties.Pressure'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

    @pytest.mark.negative
    def test_CentrifugalPump_inlet_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = CentrifugalPump()
            m4.inlet_temperature = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'inlet_temperature'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))

    @pytest.mark.negative
    def test_CentrifugalPump_outlet_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = CentrifugalPump()
            m4.outlet_temperature = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'outlet_temperature'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

    @pytest.mark.negative
    def test_CentrifugalPump_temperature_decrease_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = CentrifugalPump()
            m4.temperature_decrease = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'temperature_decrease'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

    @pytest.mark.negative
    def test_CentrifugalPump_temperature_increase_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = CentrifugalPump()
            m4.temperature_increase = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'temperature_increase'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                                                      

    @pytest.mark.negative
    def test_CentrifugalPump_design_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = CentrifugalPump()
            m4.design_temperature = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'design_temperature'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

    @pytest.mark.negative
    def test_CentrifugalPump_inlet_mass_flowrate_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = CentrifugalPump()
            m4.inlet_mass_flowrate = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'inlet_mass_flowrate'. Should be '(<class 'propylean.properties.MassFlowRate'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                   

    @pytest.mark.negative
    def test_CentrifugalPump_outlet_mass_flowrate_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = CentrifugalPump()
            m4.outlet_mass_flowrate = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'outlet_mass_flowrate'. Should be '(<class 'propylean.properties.MassFlowRate'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))

    @pytest.mark.negative
    def test_CentrifugalPump_energy_in_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = CentrifugalPump()
            m4.energy_in = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'energy_in'. Should be '(<class 'propylean.properties.Power'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))      

    @pytest.mark.negative
    def test_CentrifugalPump_energy_out_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = CentrifugalPump()
            m4.energy_out = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'energy_out'. Should be '(<class 'propylean.properties.Power'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))

    @pytest.mark.negative
    def test_CentrifugalPump_stream_connecion_disconnection_incorrect_type(self):
        cv = CentrifugalPump()
        from propylean import MaterialStream
        inlet_stream = MaterialStream(pressure=(20, 'bar'))
        inlet_stream.components = prop.Components({"water": 1})
            
        with pytest.raises(Exception) as exp:
            cv.connect_stream([inlet_stream], 'in', stream_governed=True)
        self.assertIn("Incorrect type \'<class \'list\'>\' provided to \'stream_object\'. Should be \'(<class \'propylean.streams.MaterialStream\'>, <class \'propylean.streams.EnergyStream\'>)\'.\\n            ",
                      str(exp)) 
        
        with pytest.raises(Exception) as exp:
            cv.connect_stream(inlet_stream, ['in'], stream_governed=True)
        self.assertIn("Incorrect type \'<class \'list\'>\' provided to \'direction\'. Should be \'<class \'str\'>\'.\\n            ",
                      str(exp)) 
        with pytest.raises(Exception) as exp:
            cv.connect_stream(inlet_stream, 'in', stream_governed=[True])
        self.assertIn("Incorrect type \'<class \'list\'>\' provided to \'stream_governed\'. Should be \'<class \'bool\'>\'.\\n            ",
                      str(exp)) 

        cv.connect_stream(inlet_stream, 'in', stream_governed=True)
        with pytest.raises(Exception) as exp:
            cv.disconnect_stream(stream_tag=["Inlet_cv_19"])
        self.assertIn("Incorrect type \'<class \'list\'>\' provided to \'stream_tag\'. Should be \'<class \'str\'>\'.\\n            ",
                      str(exp))    

    @pytest.mark.negative
    def test_CentrifugalPump_stream_disconnection_before_connecion(self):  
        cv = CentrifugalPump()
        from propylean import MaterialStream
        inlet_stream = MaterialStream(pressure=(20, 'bar'))
        inlet_stream.components = prop.Components({"water": 1})
        import warnings
        with warnings.catch_warnings(record=True) as exp:
            cv.disconnect_stream(inlet_stream)
         
        self.assertIn("Already there is no connection.",
                      str(exp[-1].message))   

    @pytest.mark.mapping
    def test_CentrifugalPump_stream_equipment_mapping(self):
        from propylean.equipments.abstract_equipment_classes import _material_stream_equipment_map as mse_map
        from propylean.equipments.abstract_equipment_classes import _energy_stream_equipment_map as ese_map
        pump = CentrifugalPump()
        inlet_stream = MaterialStream(pressure=(20, 'bar'))
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream()
        energy_in = EnergyStream()
        energy_out = EnergyStream()

        pump.connect_stream(inlet_stream, direction="in")
        pump.connect_stream(outlet_stream, direction="out")
        pump.connect_stream(energy_in, direction="in")
        pump.connect_stream(energy_out, direction="out")

        self.assertEqual(mse_map[inlet_stream.index][2], pump.index)
        self.assertEqual(mse_map[inlet_stream.index][3], pump.__class__)
        self.assertEqual(mse_map[outlet_stream.index][0], pump.index)
        self.assertEqual(mse_map[outlet_stream.index][1], pump.__class__) 

        self.assertEqual(ese_map[energy_in.index][2], pump.index)
        self.assertEqual(ese_map[energy_in.index][3], pump.__class__)
        self.assertEqual(ese_map[energy_out.index][0], pump.index)
        self.assertEqual(ese_map[energy_out.index][1], pump.__class__)    

        pump.disconnect_stream(inlet_stream)
        pump.disconnect_stream(outlet_stream)
        pump.disconnect_stream(energy_in)
        pump.disconnect_stream(energy_out)  

        self.assertIsNone(mse_map[inlet_stream.index][2])
        self.assertIsNone(mse_map[inlet_stream.index][3])
        self.assertIsNone(mse_map[outlet_stream.index][0])
        self.assertIsNone(mse_map[outlet_stream.index][1]) 

        self.assertIsNone(ese_map[energy_in.index][2])
        self.assertIsNone(ese_map[energy_in.index][3])
        self.assertIsNone(ese_map[energy_out.index][0])
        self.assertIsNone(ese_map[energy_out.index][1])   

    @pytest.mark.delete 
    def test_CentrifugalPump_stream_equipment_delete_without_connection(self):
        pump = CentrifugalPump()   
        print(pump)
        pump.delete()
        with pytest.raises(Exception) as exp:
            print(pump)               