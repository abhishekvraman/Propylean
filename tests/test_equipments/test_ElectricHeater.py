import pytest
import unittest
from propylean.equipments.exchangers import ElectricHeater
from propylean.streams import MaterialStream, EnergyStream
import propylean.properties as prop
import pandas as pd
from propylean.settings import Settings

class test_ElectricHeater(unittest.TestCase):
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_ElectricHeater_instantiation_only_tag(self):
        electric_heater = ElectricHeater(tag="electric_heater_1")
        self.assertEqual(electric_heater.tag, "electric_heater_1")
        self.assertEqual(electric_heater.pressure_drop, prop.Pressure(0))
        self.assertEqual(electric_heater.pressure_drop, prop.Pressure(0))
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_ElectricHeater_instantiation_tag_and_pressure_drop(self):
        electric_heater = ElectricHeater(tag="electric_heater_2",
                               pressure_drop=prop.Pressure(1, 'bar'))
        self.assertEqual(electric_heater.tag, "electric_heater_2")
        self.assertEqual(electric_heater.pressure_drop, prop.Pressure(1, 'bar'))
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_ElectricHeater_instantiation_no_arguments(self):
        electric_heater = ElectricHeater()
        self.assertIsNotNone(electric_heater.tag)
        self.assertEqual(electric_heater.pressure_drop, prop.Pressure(0))
        self.assertEqual(electric_heater.temperature_increase, prop.Temperature(0))
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_ElectricHeater_instantiation_efficiency(self):
        electric_heater = ElectricHeater(tag="electric_heater_3",
                               pressure_drop=(1, 'bar'),
                               efficiency=0.6)
        self.assertEqual(electric_heater.tag, "electric_heater_3")
        self.assertEqual(electric_heater.pressure_drop, prop.Pressure(1, 'bar'))
        self.assertEqual(electric_heater.efficiency, 0.6)
        
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_ElectricHeater_instantiation_temperature_increase(self):
        electric_heater = ElectricHeater(pressure_drop=(1, 'bar'),
                               efficiency=0.6,
                               temperature_increase=(40, "C"))
        self.assertEqual(electric_heater.pressure_drop, prop.Pressure(1, 'bar'))
        self.assertEqual(electric_heater.efficiency, 0.6)
        self.assertEqual(electric_heater.temperature_increase, prop.Temperature(40, "C"))
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_ElectricHeater_instantiation_power(self):
        electric_heater = ElectricHeater(power = (20, 'kW'))
        self.assertEqual(electric_heater.power, prop.Power(20, 'kW'))
        
    @pytest.mark.positive
    def test_ElectricHeater_representation(self):
        electric_heater = ElectricHeater(tag="electric_heater_5")
        self.assertIn("Electric Heater with tag: electric_heater_5", str(electric_heater))
    
    @pytest.mark.positive
    def test_ElectricHeater_setting_inlet_pressure(self):
        electric_heater = ElectricHeater(tag="electric_heater_6",
                               pressure_drop=(1, 'bar'))
        electric_heater.inlet_pressure = (30, 'bar')
        self.assertEqual(electric_heater.inlet_pressure, prop.Pressure(30, 'bar'))
        self.assertEqual(electric_heater.outlet_pressure, prop.Pressure(29, 'bar'))
    
    @pytest.mark.positive
    def test_ElectricHeater_setting_outlet_pressure(self):
        electric_heater = ElectricHeater(tag="electric_heater_7",
                               pressure_drop=(1, 'bar'))
        electric_heater.outlet_pressure = (40, 'bar')
        self.assertEqual(electric_heater.inlet_pressure, prop.Pressure(41, 'bar'))
        self.assertEqual(electric_heater.outlet_pressure, prop.Pressure(40, 'bar'))
    
    @pytest.mark.positive
    def test_ElectricHeater_setting_inlet_temperature(self):
        electric_heater = ElectricHeater(tag="electric_heater_8",
                               temperature_increase=(40, 'C'))
        electric_heater.inlet_temperature = (60, 'C')
        self.assertEqual(electric_heater.inlet_temperature, prop.Temperature(60, 'C'))
        self.assertEqual(electric_heater.outlet_temperature, prop.Temperature(100, 'C'))
    
    @pytest.mark.positive
    def test_ElectricHeater_setting_outlet_temperature(self):
        electric_heater = ElectricHeater(tag="electric_heater_9",
                               temperature_increase=(100, 'F'))
        electric_heater.outlet_temperature = (230, 'F')
        self.assertLess(abs(electric_heater.inlet_temperature.value-130), 0.0001)
        self.assertEqual(electric_heater.inlet_temperature.unit, 'F')
        self.assertLess(abs(electric_heater.outlet_temperature.value-230), 0.0001)
        self.assertEqual(electric_heater.outlet_temperature.unit, 'F')
    
    @pytest.mark.positive
    def test_ElectricHeater_setting_inlet_mass_flowrate(self):
        electric_heater = ElectricHeater(tag="electric_heater_10")
        electric_heater.inlet_mass_flowrate = (1000, 'kg/h')
        self.assertEqual(electric_heater.inlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
        self.assertEqual(electric_heater.outlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
    
    @pytest.mark.positive
    def test_ElectricHeater_setting_outlet_mass_flowrate(self):
        electric_heater = ElectricHeater(tag="electric_heater_11")
        electric_heater.outlet_mass_flowrate = (1000, 'kg/h')
        self.assertEqual(electric_heater.inlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
        self.assertEqual(electric_heater.outlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
    
    @pytest.mark.positive
    def test_ElectricHeater_connection_with_material_stream_inlet_stream_governed(self):
        electric_heater = ElectricHeater(tag="electric_heater_12",
                               pressure_drop=(1, 'bar'),
                               temperature_increase=prop.Temperature(25, 'K'))
        inlet_stream = MaterialStream(tag="Inlet_electric_heater_12",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(50, 'C'))
        # Test connection is made.
        self.assertTrue(electric_heater.connect_stream(inlet_stream, 'in', stream_governed=True))
        # Test inlet properties of electric_heater are equal to inlet stream's.
        self.assertEqual(electric_heater.inlet_pressure, inlet_stream.pressure)
        self.assertEqual(electric_heater.inlet_temperature, inlet_stream.temperature)
        self.assertEqual(electric_heater.inlet_mass_flowrate, inlet_stream.mass_flowrate)
        # Test outlet properties are calculated accordingly.
        self.assertEqual(electric_heater.outlet_pressure, electric_heater.inlet_pressure-electric_heater.pressure_drop)
        self.assertEqual(electric_heater.inlet_temperature.value + 25, 
                         electric_heater.outlet_temperature.value)
        self.assertEqual(electric_heater.inlet_temperature.unit, electric_heater.outlet_temperature.unit)
        self.assertEqual(electric_heater.inlet_mass_flowrate, electric_heater.outlet_mass_flowrate)

    @pytest.mark.positive
    def test_ElectricHeater_connection_with_material_stream_outlet_stream_governed(self):
        electric_heater = ElectricHeater(tag="electric_heater_13",
                               pressure_drop=(10, 'bar'),
                               temperature_increase=prop.Temperature(25, 'F'))
        outlet_stream = MaterialStream(tag="Outlet_electric_heater_13",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(130, 'F'))
        # Test connection is made.
        self.assertTrue(electric_heater.connect_stream(outlet_stream, 'out', stream_governed=True))
        # Test outlet properties of electric_heater are equal to outlet stream's.
        self.assertEqual(electric_heater.outlet_pressure, outlet_stream.pressure)
        self.assertEqual(electric_heater.outlet_temperature, outlet_stream.temperature)
        self.assertEqual(electric_heater.outlet_mass_flowrate, outlet_stream.mass_flowrate)
        # Test intlet properties are calculated accordingly.
        self.assertEqual(electric_heater.inlet_pressure, electric_heater.outlet_pressure+electric_heater.pressure_drop)
        self.assertEqual(electric_heater.inlet_temperature.value, 
                         electric_heater.outlet_temperature.value - 25)
        self.assertEqual(electric_heater.inlet_mass_flowrate, electric_heater.outlet_mass_flowrate)

    @pytest.mark.positive
    def test_ElectricHeater_connection_with_material_stream_inlet_equipment_governed(self):
        electric_heater = ElectricHeater(tag="electric_heater_14",
                               pressure_drop=(1, 'bar'),
                               temperature_increase=(10, "C"))

        electric_heater.inlet_pressure = (30, 'bar')
        electric_heater.inlet_mass_flowrate = (1000, 'kg/h')
        electric_heater.inlet_temperature = (320, 'K')
        inlet_stream = MaterialStream(tag="Inlet_electric_heater_14")
        # Test connection is made.
        self.assertTrue(electric_heater.connect_stream(inlet_stream, 'in', stream_governed=False))
        # Test inlet properties of electric_heater are equal to inlet stream's.
        self.assertEqual(electric_heater.inlet_pressure, inlet_stream.pressure)
        self.assertEqual(electric_heater.inlet_temperature, inlet_stream.temperature)
        self.assertEqual(electric_heater.inlet_mass_flowrate, inlet_stream.mass_flowrate)
        # Test outlet properties are calculated accordingly.
        self.assertEqual(electric_heater.outlet_pressure, electric_heater.inlet_pressure-electric_heater.pressure_drop)
        self.assertEqual(electric_heater.inlet_temperature.value + 10, 
                         electric_heater.outlet_temperature.value)
        self.assertEqual(electric_heater.inlet_mass_flowrate, electric_heater.outlet_mass_flowrate)

    @pytest.mark.positive
    def test_ElectricHeater_connection_with_material_stream_outlet_equipment_governed(self):
        electric_heater = ElectricHeater(tag="electric_heater_15",
                               pressure_drop=(1, 'bar'),
                               temperature_increase=(40, "C"))
        electric_heater.outlet_pressure = (130, 'bar')
        electric_heater.outlet_mass_flowrate = (1000, 'kg/h')
        electric_heater.outlet_temperature = (70, 'C')
        outlet_stream = MaterialStream(tag="Outlet_electric_heater_15")
        # Test connection is made.
        self.assertTrue(electric_heater.connect_stream(outlet_stream, 'out', stream_governed=False))
        # Test outlet properties of electric_heater are equal to outlet stream's.
        self.assertEqual(electric_heater.outlet_pressure, outlet_stream.pressure)
        self.assertEqual(electric_heater.outlet_temperature, outlet_stream.temperature)
        self.assertEqual(electric_heater.outlet_mass_flowrate, outlet_stream.mass_flowrate)
        # Test intlet properties are calculated accordingly.
        self.assertEqual(electric_heater.inlet_pressure, electric_heater.outlet_pressure+electric_heater.pressure_drop)
        self.assertEqual(electric_heater.inlet_temperature.value, 30)
        self.assertEqual(electric_heater.inlet_mass_flowrate, electric_heater.outlet_mass_flowrate)
    
    # TODO Uncomment below when power setting feature is provided.
    # @pytest.mark.positive
    # def test_ElectricHeater_connection_with_energy_stream_inlet_stream_governed(self):
    #     electric_heater = ElectricHeater(tag="electric_heater_16",
    #                            pressure_drop=(10, 'bar'))
    #     electric_heater_power = EnergyStream(tag="Power_electric_heater_16", amount=(10,"MW"))
    #     # Test connection is made.
    #     self.assertTrue(electric_heater.connect_stream(electric_heater_power, stream_governed=True))
    #     # Test inlet properties of electric_heater are equal to outlet stream's.
    #     self.assertEqual(electric_heater.power, electric_heater_power.amount)
    #     self.assertEqual(electric_heater.power, electric_heater_power.unit)

    @pytest.mark.positive
    def test_ElectricHeater_connection_with_energy_stream_inlet_equipment_governed(self):
        electric_heater = ElectricHeater(tag="electric_heater_17",
                               pressure_drop=(10, 'bar'))
        electric_heater_power = EnergyStream(tag="Power_electric_heater_17", amount=(10, "MW"))
        electric_heater_inlet = MaterialStream(mass_flowrate=(1000, 'kg/h'),
                                          pressure=(30, 'bar'),
                                          temperature=(25, 'C'))
        electric_heater_inlet.isentropic_exponent = 1.36952
        electric_heater_inlet.Z_g = 0.94024
        electric_heater_inlet.molecular_weight = prop.MolecularWeigth(16.043, 'g/mol')
        # Test connection is made.
        self.assertTrue(electric_heater.connect_stream(electric_heater_inlet, "in", stream_governed=False))
        self.assertTrue(electric_heater.connect_stream(electric_heater_power, "in"))
        # Test inlet properties of electric_heater are equal to outlet stream's.
        self.assertAlmostEqual(electric_heater.power.value, electric_heater_power.amount.value)
        self.assertEqual(electric_heater.power.unit, electric_heater_power.amount.unit)
    
    @pytest.mark.positive
    def test_ElectricHeater_stream_disconnection_by_stream_object(self):
        electric_heater = ElectricHeater(tag="electric_heater_18",
                               pressure_drop=(10, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_electric_heater_18")
        inlet_stream.isentropic_exponent = 1.36952
        inlet_stream.Z_g = 0.94024
        inlet_stream.molecular_weight = prop.MolecularWeigth(16.043, 'g/mol')
        outlet_stream = MaterialStream(tag="Outlet_electric_heater_18")
        electric_heater_power = EnergyStream(tag="power_electric_heater_18")
        # Test connection is made.
        self.assertTrue(electric_heater.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(electric_heater.connect_stream(outlet_stream, 'out', stream_governed=False))
        self.assertTrue(electric_heater.connect_stream(electric_heater_power, "in"))
        # Test disconnection
        self.assertTrue(electric_heater.disconnect_stream(inlet_stream))
        self.assertTrue(electric_heater.disconnect_stream(outlet_stream))
        self.assertTrue(electric_heater.disconnect_stream(electric_heater_power))
        self.assertIsNone(electric_heater._inlet_material_stream_tag)
        self.assertIsNone(electric_heater._outlet_material_stream_tag)
        self.assertIsNone(electric_heater._inlet_energy_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)
    
    @pytest.mark.positive
    def test_ElectricHeater_stream_disconnection_by_stream_tag(self):
        electric_heater = ElectricHeater(tag="electric_heater_19",
                               pressure_drop=(10, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_electric_heater_19")
        inlet_stream.isentropic_exponent = 1.36952
        inlet_stream.Z_g = 0.94024
        inlet_stream.molecular_weight = prop.MolecularWeigth(16.043, 'g/mol')
        outlet_stream = MaterialStream(tag="Outlet_electric_heater_19")
        electric_heater_power = EnergyStream(tag="power_electric_heater_19")
        # Test connection is made.
        self.assertTrue(electric_heater.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(electric_heater.connect_stream(outlet_stream, 'out', stream_governed=False))
        self.assertEqual(inlet_stream.components, outlet_stream.components)
        self.assertTrue(electric_heater.connect_stream(electric_heater_power, "in"))
        # Test disconnection
        self.assertTrue(electric_heater.disconnect_stream(stream_tag="Inlet_electric_heater_19"))
        self.assertTrue(electric_heater.disconnect_stream(stream_tag="Outlet_electric_heater_19"))
        self.assertTrue(electric_heater.disconnect_stream(stream_tag="power_electric_heater_19"))
        self.assertIsNone(electric_heater._inlet_material_stream_tag)
        self.assertIsNone(electric_heater._outlet_material_stream_tag)
        self.assertIsNone(electric_heater._inlet_energy_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)
    
    @pytest.mark.positive
    def test_ElectricHeater_stream_disconnection_by_direction_stream_type(self):
        electric_heater = ElectricHeater(tag="electric_heater_20",
                               pressure_drop=(10, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_electric_heater_20")
        inlet_stream.isentropic_exponent = 1.36952
        inlet_stream.Z_g = 0.94024
        inlet_stream.molecular_weight = prop.MolecularWeigth(16.043, 'g/mol')
        outlet_stream = MaterialStream(tag="Outlet_electric_heater_20")
        electric_heater_power = EnergyStream(tag="power_electric_heater_20")
        # Test connection is made.
        self.assertTrue(electric_heater.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(electric_heater.connect_stream(outlet_stream, 'out', stream_governed=False))
        self.assertTrue(electric_heater.connect_stream(electric_heater_power, "in"))
        # Test disconnection
        self.assertTrue(electric_heater.disconnect_stream(direction="In", stream_type="Material"))
        self.assertTrue(electric_heater.disconnect_stream(direction="ouTlet", stream_type="materiaL"))
        self.assertTrue(electric_heater.disconnect_stream(stream_type="energy"))
        self.assertIsNone(electric_heater._inlet_material_stream_tag)
        self.assertIsNone(electric_heater._outlet_material_stream_tag)
        self.assertIsNone(electric_heater._inlet_energy_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)
