import pytest
import unittest
from propylean.equipments import CentrifugalPump
from propylean.streams import MaterialStream, EnergyStream
import propylean.properties as prop
import pandas as pd
from unittest.mock import patch

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
        self.assertEqual(pump.efficiency, 70)
    
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
        self.assertEqual(pump.inlet_temperature, inlet_stream.temperature)
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
        self.assertEqual(pump.outlet_temperature, outlet_stream.temperature)
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
    
    @pytest.mark.positive
    def test_CentrifugalPump_connection_with_energy_stream_inlet_stream_governed(self):
        pump = CentrifugalPump(tag="Pump_16",
                               differential_pressure=(100, 'bar'))
        pump_power = EnergyStream(tag="Power_Pump_16", amount=(10,"MW"))
        # Test connection is made.
        self.assertTrue(pump.connect_stream(pump_power, 'out', stream_governed=True))
        # Test inlet properties of pump are equal to outlet stream's.
        self.assertEqual(pump.energy_in.value, pump_power.amount)
        self.assertEqual(pump.power.unit, pump_power.unit)

    pytest.mark.positive
    def test_CentrifugalPump_connection_with_energy_stream_inlet_equipment_governed(self):
        pump = CentrifugalPump(tag="Pump_17",
                               differential_pressure=(100, 'bar'))
        pump_power = EnergyStream(tag="Power_Pump_17", amount=(10,"MW"))
        # Test connection is made.
        self.assertTrue(pump.connect_stream(pump_power, 'out', stream_governed=False))
        # Test inlet properties of pump are equal to outlet stream's.
        self.assertEqual(pump.power.value, pump_power.value)
        self.assertEqual(pump.power.unit, pump_power.unit)
    
    @pytest.mark.positive
    def test_CentrifugalPump_stream_disconnection_by_stream_object(self):
        pump = CentrifugalPump(tag="Pump_18",
                               differential_pressure=(100, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_Pump_18")
        outlet_stream = MaterialStream(tag="Outlet_Pump_18")
        pump_power = EnergyStream(tag="Power_Pump_18")
        # Test connection is made.
        self.assertTrue(pump.connect_stream(inlet_stream, 'in', stream_governed=False))
        self.assertTrue(pump.connect_stream(outlet_stream, 'out', stream_governed=False))
        self.assertTrue(pump.connect_stream(pump_power))
        # Test disconnection
        self.assertTrue(pump.disconnect_stream(inlet_stream))
        self.assertTrue(pump.disconnect_stream(outlet_stream))
        self.assertTrue(pump.disconnect_stream(pump_power))
        self.assertIsNone(pump._inlet_material_stream_tag)
        self.assertIsNone(pump._outlet_material_stream_tag)
        self.assertIsNone(pump._inlet_energy_stream_tag)
        self.assertRaises(AttributeError, pump._outlet_energy_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)
    
    @pytest.mark.positive
    def test_CentrifugalPump_stream_disconnection_by_stream_tag(self):
        pump = CentrifugalPump(tag="Pump_19",
                               differential_pressure=(100, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_Pump_19")
        outlet_stream = MaterialStream(tag="Outlet_Pump_19")
        pump_power = EnergyStream(tag="Power_Pump_19")
        # Test connection is made.
        self.assertTrue(pump.connect_stream(inlet_stream, 'in', stream_governed=False))
        self.assertTrue(pump.connect_stream(outlet_stream, 'out', stream_governed=False))
        self.assertTrue(pump.connect_stream(pump_power))
        # Test disconnection
        self.assertTrue(pump.disconnect_stream(stream_tag="Inlet_Pump_19"))
        self.assertTrue(pump.disconnect_stream(stream_tag="Outlet_Pump_19"))
        self.assertTrue(pump.disconnect_stream(stream_tag="Power_Pump_19"))
        self.assertIsNone(pump._inlet_material_stream_tag)
        self.assertIsNone(pump._outlet_material_stream_tag)
        self.assertIsNone(pump._inlet_energy_stream_tag)
        self.assertRaises(AttributeError, pump._outlet_energy_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)
    
    @pytest.mark.positive
    def test_CentrifugalPump_stream_disconnection_by_direction_stream_type(self):
        pump = CentrifugalPump(tag="Pump_20",
                               differential_pressure=(100, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_Pump_20")
        outlet_stream = MaterialStream(tag="Outlet_Pump_20")
        pump_power = EnergyStream(tag="Power_Pump_20")
        # Test connection is made.
        self.assertTrue(pump.connect_stream(inlet_stream, 'in', stream_governed=False))
        self.assertTrue(pump.connect_stream(outlet_stream, 'out', stream_governed=False))
        self.assertTrue(pump.connect_stream(pump_power))
        # Test disconnection
        self.assertTrue(pump.disconnect_stream(direction="In", stream_type="Material"))
        self.assertTrue(pump.disconnect_stream(direction="ouTlet", stream_type="materiaL"))
        self.assertTrue(pump.disconnect_stream(stream_type="energy"))
        self.assertIsNone(pump._inlet_material_stream_tag)
        self.assertIsNone(pump._outlet_material_stream_tag)
        self.assertIsNone(pump._inlet_energy_stream_tag)
        self.assertRaises(AttributeError, pump._outlet_energy_stream_tag)
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
        inlet_stream.components = {"water": 100}
        pump.connect_stream(inlet_stream, 'in', stream_governed=True)
        pressure = prop.Pressure(100, 'bar')
        pressure.unit = "Pa"
        expected_head_value = pressure.value / (9.8 * inlet_stream.density.value)
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
        inlet_stream.compound_amounts = {"water": 100}
        pump.connect_stream(inlet_stream, 'in', stream_governed=True)
        pressure = prop.Pressure(100, 'bar')
        pressure.unit = "Pa"
        expected_hydraulic_power = prop.Power(10023.2, "W")
        expected_brake_horse_power = expected_hydraulic_power.value/pump.efficiency
        pump_hydraulic_power = pump.hydraulic_power
        pump_hydraulic_power.unit = "W"
        pump_brake_horse_power = pump.brake_horse_power
        pump_brake_horse_power.unit = "W"
        self.assertAlmostEqual(expected_hydraulic_power, pump_hydraulic_power.value)
        self.assertAlmostEqual(expected_brake_horse_power, pump_brake_horse_power.value)

