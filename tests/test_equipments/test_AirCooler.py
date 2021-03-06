import pytest
import unittest
from propylean.equipments.exchangers import AirCooler
from propylean.streams import MaterialStream, EnergyStream
import propylean.properties as prop
import pandas as pd
from propylean.settings import Settings

class test_AirCooler(unittest.TestCase):
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_AirCooler_instantiation_only_tag(self):
        air_cooler = AirCooler(tag="air_cooler_1")
        self.assertEqual(air_cooler.tag, "air_cooler_1")
        self.assertEqual(air_cooler.pressure_drop, prop.Pressure(0))
        self.assertEqual(air_cooler.pressure_drop, prop.Pressure(0))
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_AirCooler_instantiation_tag_and_pressure_drop(self):
        air_cooler = AirCooler(tag="air_cooler_2",
                               pressure_drop=prop.Pressure(1, 'bar'))
        self.assertEqual(air_cooler.tag, "air_cooler_2")
        self.assertEqual(air_cooler.pressure_drop, prop.Pressure(1, 'bar'))
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_AirCooler_instantiation_no_arguments(self):
        air_cooler = AirCooler()
        self.assertIsNotNone(air_cooler.tag)
        self.assertEqual(air_cooler.pressure_drop, prop.Pressure(0))
        self.assertEqual(air_cooler.temperature_decrease, prop.Temperature(0))
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_AirCooler_instantiation_efficiency(self):
        air_cooler = AirCooler(tag="air_cooler_3",
                               pressure_drop=(1, 'bar'),
                               efficiency=0.6)
        self.assertEqual(air_cooler.tag, "air_cooler_3")
        self.assertEqual(air_cooler.pressure_drop, prop.Pressure(1, 'bar'))
        self.assertEqual(air_cooler.efficiency, 0.6)
        
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_AirCooler_instantiation_temperature_decrease(self):
        air_cooler = AirCooler(pressure_drop=(1, 'bar'),
                               efficiency=0.6,
                               temperature_decrease=(40, "C"))
        self.assertEqual(air_cooler.pressure_drop, prop.Pressure(1, 'bar'))
        self.assertEqual(air_cooler.efficiency, 0.6)
        self.assertEqual(air_cooler.temperature_decrease, prop.Temperature(40, "C"))
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_AirCooler_instantiation_fan_power(self):
        air_cooler = AirCooler(fan_power = (20, 'kW'))
        self.assertEqual(air_cooler.fan_power, prop.Power(20, 'kW'))
        
    @pytest.mark.positive
    def test_AirCooler_representation(self):
        air_cooler = AirCooler(tag="air_cooler_5")
        self.assertIn("Air Cooler with tag: air_cooler_5", str(air_cooler))
    
    @pytest.mark.positive
    def test_AirCooler_setting_inlet_pressure(self):
        air_cooler = AirCooler(tag="air_cooler_6",
                               pressure_drop=(1, 'bar'))
        air_cooler.inlet_pressure = (30, 'bar')
        self.assertEqual(air_cooler.inlet_pressure, prop.Pressure(30, 'bar'))
        self.assertEqual(air_cooler.outlet_pressure, prop.Pressure(29, 'bar'))
    
    @pytest.mark.positive
    def test_AirCooler_setting_outlet_pressure(self):
        air_cooler = AirCooler(tag="air_cooler_7",
                               pressure_drop=(1, 'bar'))
        air_cooler.outlet_pressure = (40, 'bar')
        self.assertEqual(air_cooler.inlet_pressure, prop.Pressure(41, 'bar'))
        self.assertEqual(air_cooler.outlet_pressure, prop.Pressure(40, 'bar'))
    
    @pytest.mark.positive
    def test_AirCooler_setting_inlet_temperature(self):
        air_cooler = AirCooler(tag="air_cooler_8",
                               temperature_decrease=(40, 'C'))
        air_cooler.inlet_temperature = (100, 'C')
        self.assertEqual(air_cooler.inlet_temperature, prop.Temperature(100, 'C'))
        self.assertEqual(air_cooler.outlet_temperature, prop.Temperature(60, 'C'))
    
    @pytest.mark.positive
    def test_AirCooler_setting_outlet_temperature(self):
        air_cooler = AirCooler(tag="air_cooler_9",
                               temperature_decrease=(100, 'F'))
        air_cooler.outlet_temperature = (230, 'F')
        self.assertLess(abs(air_cooler.inlet_temperature.value-330), 0.0001)
        self.assertEqual(air_cooler.inlet_temperature.unit, 'F')
        self.assertLess(abs(air_cooler.outlet_temperature.value-230), 0.0001)
        self.assertEqual(air_cooler.outlet_temperature.unit, 'F')
    
    @pytest.mark.positive
    def test_AirCooler_setting_inlet_mass_flowrate(self):
        air_cooler = AirCooler(tag="air_cooler_10")
        air_cooler.inlet_mass_flowrate = (1000, 'kg/h')
        self.assertEqual(air_cooler.inlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
        self.assertEqual(air_cooler.outlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
    
    @pytest.mark.positive
    def test_AirCooler_setting_outlet_mass_flowrate(self):
        air_cooler = AirCooler(tag="air_cooler_11")
        air_cooler.outlet_mass_flowrate = (1000, 'kg/h')
        self.assertEqual(air_cooler.inlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
        self.assertEqual(air_cooler.outlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
    
    @pytest.mark.positive
    def test_AirCooler_connection_with_material_stream_inlet_stream_governed(self):
        air_cooler = AirCooler(tag="air_cooler_12",
                               pressure_drop=(1, 'bar'),
                               temperature_decrease=prop.Temperature(25, 'K'))
        inlet_stream = MaterialStream(tag="Inlet_air_cooler_12",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(50, 'C'))
        # Test connection is made.
        self.assertTrue(air_cooler.connect_stream(inlet_stream, 'in', stream_governed=True))
        # Test inlet properties of air_cooler are equal to inlet stream's.
        self.assertEqual(air_cooler.inlet_pressure, inlet_stream.pressure)
        self.assertEqual(air_cooler.inlet_temperature, inlet_stream.temperature)
        self.assertEqual(air_cooler.inlet_mass_flowrate, inlet_stream.mass_flowrate)
        # Test outlet properties are calculated accordingly.
        self.assertEqual(air_cooler.outlet_pressure, air_cooler.inlet_pressure-air_cooler.pressure_drop)
        self.assertEqual(air_cooler.inlet_temperature.value - 25, 
                         air_cooler.outlet_temperature.value)
        self.assertEqual(air_cooler.inlet_temperature.unit, air_cooler.outlet_temperature.unit)
        self.assertEqual(air_cooler.inlet_mass_flowrate, air_cooler.outlet_mass_flowrate)

    @pytest.mark.positive
    def test_AirCooler_connection_with_material_stream_outlet_stream_governed(self):
        air_cooler = AirCooler(tag="air_cooler_13",
                               pressure_drop=(10, 'bar'),
                               temperature_decrease=prop.Temperature(25, 'F'))
        outlet_stream = MaterialStream(tag="Outlet_air_cooler_13",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(130, 'F'))
        # Test connection is made.
        self.assertTrue(air_cooler.connect_stream(outlet_stream, 'out', stream_governed=True))
        # Test outlet properties of air_cooler are equal to outlet stream's.
        self.assertEqual(air_cooler.outlet_pressure, outlet_stream.pressure)
        self.assertEqual(air_cooler.outlet_temperature, outlet_stream.temperature)
        self.assertEqual(air_cooler.outlet_mass_flowrate, outlet_stream.mass_flowrate)
        # Test intlet properties are calculated accordingly.
        self.assertEqual(air_cooler.inlet_pressure, air_cooler.outlet_pressure+air_cooler.pressure_drop)
        self.assertEqual(air_cooler.inlet_temperature.value, 
                         air_cooler.outlet_temperature.value + 25)
        self.assertEqual(air_cooler.inlet_mass_flowrate, air_cooler.outlet_mass_flowrate)

    @pytest.mark.positive
    def test_AirCooler_connection_with_material_stream_inlet_equipment_governed(self):
        air_cooler = AirCooler(tag="air_cooler_14",
                               pressure_drop=(1, 'bar'),
                               temperature_decrease=(10, "C"))

        air_cooler.inlet_pressure = (30, 'bar')
        air_cooler.inlet_mass_flowrate = (1000, 'kg/h')
        air_cooler.inlet_temperature = (320, 'K')
        inlet_stream = MaterialStream(tag="Inlet_air_cooler_14")
        # Test connection is made.
        self.assertTrue(air_cooler.connect_stream(inlet_stream, 'in', stream_governed=False))
        # Test inlet properties of air_cooler are equal to inlet stream's.
        self.assertEqual(air_cooler.inlet_pressure, inlet_stream.pressure)
        self.assertEqual(air_cooler.inlet_temperature, inlet_stream.temperature)
        self.assertEqual(air_cooler.inlet_mass_flowrate, inlet_stream.mass_flowrate)
        # Test outlet properties are calculated accordingly.
        self.assertEqual(air_cooler.outlet_pressure, air_cooler.inlet_pressure-air_cooler.pressure_drop)
        self.assertEqual(air_cooler.inlet_temperature.value - 10, 
                         air_cooler.outlet_temperature.value)
        self.assertEqual(air_cooler.inlet_mass_flowrate, air_cooler.outlet_mass_flowrate)

    @pytest.mark.positive
    def test_AirCooler_connection_with_material_stream_outlet_equipment_governed(self):
        air_cooler = AirCooler(tag="air_cooler_15",
                               pressure_drop=(1, 'bar'),
                               temperature_decrease=(10, "C"))
        air_cooler.outlet_pressure = (130, 'bar')
        air_cooler.outlet_mass_flowrate = (1000, 'kg/h')
        air_cooler.outlet_temperature = (30, 'C')
        outlet_stream = MaterialStream(tag="Outlet_air_cooler_15")
        # Test connection is made.
        self.assertTrue(air_cooler.connect_stream(outlet_stream, 'out', stream_governed=False))
        # Test outlet properties of air_cooler are equal to outlet stream's.
        self.assertEqual(air_cooler.outlet_pressure, outlet_stream.pressure)
        self.assertEqual(air_cooler.outlet_temperature, outlet_stream.temperature)
        self.assertEqual(air_cooler.outlet_mass_flowrate, outlet_stream.mass_flowrate)
        # Test intlet properties are calculated accordingly.
        self.assertEqual(air_cooler.inlet_pressure, air_cooler.outlet_pressure+air_cooler.pressure_drop)
        self.assertEqual(air_cooler.inlet_temperature.value, 40)
        self.assertEqual(air_cooler.inlet_mass_flowrate, air_cooler.outlet_mass_flowrate)
    
    # TODO Uncomment below when power setting feature is provided.
    # @pytest.mark.positive
    # def test_AirCooler_connection_with_energy_stream_inlet_stream_governed(self):
    #     air_cooler = AirCooler(tag="air_cooler_16",
    #                            pressure_drop=(10, 'bar'))
    #     air_cooler_fan_power = EnergyStream(tag="Power_air_cooler_16", amount=(10,"MW"))
    #     # Test connection is made.
    #     self.assertTrue(air_cooler.connect_stream(air_cooler_fan_power, stream_governed=True))
    #     # Test inlet properties of air_cooler are equal to outlet stream's.
    #     self.assertEqual(air_cooler.fan_power, air_cooler_fan_power.amount)
    #     self.assertEqual(air_cooler.power, air_cooler_fan_power.unit)

    @pytest.mark.positive
    def test_AirCooler_connection_with_energy_stream_inlet_equipment_governed(self):
        air_cooler = AirCooler(tag="air_cooler_17",
                               pressure_drop=(10, 'bar'))
        air_cooler_fan_power = EnergyStream(tag="Power_air_cooler_17", amount=(10, "MW"))
        air_cooler_inlet = MaterialStream(mass_flowrate=(1000, 'kg/h'),
                                          pressure=(30, 'bar'),
                                          temperature=(25, 'C'))
        air_cooler_inlet.isentropic_exponent = 1.36952
        air_cooler_inlet.Z_g = 0.94024
        air_cooler_inlet.molecular_weight = prop.MolecularWeigth(16.043, 'g/mol')
        # Test connection is made.
        self.assertTrue(air_cooler.connect_stream(air_cooler_inlet, "in", stream_governed=False))
        self.assertTrue(air_cooler.connect_stream(air_cooler_fan_power, "in"))
        # Test inlet properties of air_cooler are equal to outlet stream's.
        self.assertAlmostEqual(air_cooler.fan_power.value, air_cooler_fan_power.amount.value)
        self.assertEqual(air_cooler.fan_power.unit, air_cooler_fan_power.amount.unit)
    
    @pytest.mark.positive
    def test_AirCooler_stream_disconnection_by_stream_object(self):
        air_cooler = AirCooler(tag="air_cooler_18",
                               pressure_drop=(10, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_air_cooler_18")
        inlet_stream.isentropic_exponent = 1.36952
        inlet_stream.Z_g = 0.94024
        inlet_stream.molecular_weight = prop.MolecularWeigth(16.043, 'g/mol')
        outlet_stream = MaterialStream(tag="Outlet_air_cooler_18")
        air_cooler_fan_power = EnergyStream(tag="fan_power_air_cooler_18")
        # Test connection is made.
        self.assertTrue(air_cooler.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(air_cooler.connect_stream(outlet_stream, 'out', stream_governed=False))
        self.assertTrue(air_cooler.connect_stream(air_cooler_fan_power, "in"))
        # Test disconnection
        self.assertTrue(air_cooler.disconnect_stream(inlet_stream))
        self.assertTrue(air_cooler.disconnect_stream(outlet_stream))
        self.assertTrue(air_cooler.disconnect_stream(air_cooler_fan_power))
        self.assertIsNone(air_cooler._inlet_material_stream_tag)
        self.assertIsNone(air_cooler._outlet_material_stream_tag)
        self.assertIsNone(air_cooler._inlet_energy_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)
    
    @pytest.mark.positive
    def test_AirCooler_stream_disconnection_by_stream_tag(self):
        air_cooler = AirCooler(tag="air_cooler_19",
                               pressure_drop=(10, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_air_cooler_19")
        inlet_stream.isentropic_exponent = 1.36952
        inlet_stream.Z_g = 0.94024
        inlet_stream.molecular_weight = prop.MolecularWeigth(16.043, 'g/mol')
        outlet_stream = MaterialStream(tag="Outlet_air_cooler_19")
        air_cooler_fan_power = EnergyStream(tag="fan_power_air_cooler_19")
        # Test connection is made.
        self.assertTrue(air_cooler.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(air_cooler.connect_stream(outlet_stream, 'out', stream_governed=False))
        self.assertEqual(inlet_stream.components, outlet_stream.components)
        self.assertTrue(air_cooler.connect_stream(air_cooler_fan_power, "in"))
        # Test disconnection
        self.assertTrue(air_cooler.disconnect_stream(stream_tag="Inlet_air_cooler_19"))
        self.assertTrue(air_cooler.disconnect_stream(stream_tag="Outlet_air_cooler_19"))
        self.assertTrue(air_cooler.disconnect_stream(stream_tag="fan_power_air_cooler_19"))
        self.assertIsNone(air_cooler._inlet_material_stream_tag)
        self.assertIsNone(air_cooler._outlet_material_stream_tag)
        self.assertIsNone(air_cooler._inlet_energy_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)
    
    @pytest.mark.positive
    def test_AirCooler_stream_disconnection_by_direction_stream_type(self):
        air_cooler = AirCooler(tag="air_cooler_20",
                               pressure_drop=(10, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_air_cooler_20")
        inlet_stream.isentropic_exponent = 1.36952
        inlet_stream.Z_g = 0.94024
        inlet_stream.molecular_weight = prop.MolecularWeigth(16.043, 'g/mol')
        outlet_stream = MaterialStream(tag="Outlet_air_cooler_20")
        air_cooler_fan_power = EnergyStream(tag="fan_power_air_cooler_20")
        # Test connection is made.
        self.assertTrue(air_cooler.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(air_cooler.connect_stream(outlet_stream, 'out', stream_governed=False))
        self.assertTrue(air_cooler.connect_stream(air_cooler_fan_power, "in"))
        # Test disconnection
        self.assertTrue(air_cooler.disconnect_stream(direction="In", stream_type="Material"))
        self.assertTrue(air_cooler.disconnect_stream(direction="ouTlet", stream_type="materiaL"))
        self.assertTrue(air_cooler.disconnect_stream(stream_type="energy"))
        self.assertIsNone(air_cooler._inlet_material_stream_tag)
        self.assertIsNone(air_cooler._outlet_material_stream_tag)
        self.assertIsNone(air_cooler._inlet_energy_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)
