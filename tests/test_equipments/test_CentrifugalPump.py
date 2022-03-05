import pytest
import unittest
from propylean.equipments import CentrifugalPump
import propylean.properties as prop
import pandas as pd

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
        self.assertEqual(pump.performace_curve, performance_curve)

                             