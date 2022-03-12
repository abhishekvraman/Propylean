import pytest
import unittest
from propylean.equipments import CentrifugalPump
from propylean.streams import MaterialStream
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
        self.assertEqual(pump.inlet_temperature, prop.Temperature(130, 'F'))
        self.assertEqual(pump.outlet_temperature, prop.Temperature(130, 'F'))
    
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
    def test_CentrifugalPump_connection_with_stream_inlet_stream_governed(self):
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
        # Test outlet properties are calulcated accordingly.
        self.assertEqual(pump.outlet_pressure, pump.inlet_pressure+pump.differential_pressure)
        self.assertEqual(pump.inlet_temperature, pump.outlet_temperature)
        self.assertEqual(pump.inlet_mass_flowrate, pump.outlet_mass_flowrate)

    @pytest.mark.positive
    def test_CentrifugalPump_connection_with_stream_outlet_stream_governed(self):
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
        # Test intlet properties are calulcated accordingly.
        self.assertEqual(pump.inlet_pressure, pump.outlet_pressure-pump.differential_pressure)
        self.assertEqual(pump.inlet_temperature, pump.outlet_temperature)
        self.assertEqual(pump.inlet_mass_flowrate, pump.outlet_mass_flowrate)

    @pytest.mark.positive
    def test_CentrifugalPump_connection_with_stream_inlet_equipment_governed(self):
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
        # Test outlet properties are calulcated accordingly.
        self.assertEqual(pump.outlet_pressure, pump.inlet_pressure+pump.differential_pressure)
        self.assertEqual(pump.inlet_temperature, pump.outlet_temperature)
        self.assertEqual(pump.inlet_mass_flowrate, pump.outlet_mass_flowrate)

    @pytest.mark.positive
    def test_CentrifugalPump_connection_with_stream_outlet_equipment_governed(self):
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
        # Test intlet properties are calulcated accordingly.
        self.assertEqual(pump.inlet_pressure, pump.outlet_pressure-pump.differential_pressure)
        self.assertEqual(pump.inlet_temperature, pump.outlet_temperature)
        self.assertEqual(pump.inlet_mass_flowrate, pump.outlet_mass_flowrate)

    @pytest.mark.positive
    def test_CentrifugalPump_head_calulcation(self):
        pump = CentrifugalPump(tag="Pump_16",
                               differential_pressure=(100, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_Pump_16",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(25, 'C'))
        inlet_stream.compound_amounts = {"water": 100}
        pump.connect_stream(inlet_stream, 'in', stream_governed=True)
        pressure = prop.Pressure(100, 'bar')
        pressure.unit = "Pa"
        expected_head_value = pressure.value / (9.8 * inlet_stream.density)
        pump_head = pump.head
        pump_head.unit = "m"
        self.assertAlmostEqual(expected_head_value, pump_head.value)
