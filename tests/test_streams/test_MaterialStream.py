import pytest
import unittest
from propylean.streams import MaterialStream
import propylean.properties as prop
import pandas as pd

class test_MaterialStream(unittest.TestCase):
    def test_MaterialStream_instantiation_tag_only(self):
        m1 = MaterialStream(tag="m1")
        self.assertEqual(m1.tag, "m1")
        self.assertEqual(m1.pressure, prop.Pressure())
        self.assertEqual(m1.temperature, prop.Temperature())
        self.assertEqual(m1.mass_flowrate, prop.MassFlowRate())
        self.assertIsNone(m1.from_equipment)
        self.assertIsNone(m1.to_equipment)
    
    def test_MaterialStream_instantiation_all_properties(self):
        m2 = MaterialStream(tag="m2", 
                            pressure=(10, 'bar'),
                            temperature=300,
                            mass_flowrate=prop.MassFlowRate(1000, "kg/h"))
        self.assertEqual(m2.pressure, prop.Pressure(10, 'bar'))
        self.assertEqual(m2.temperature, prop.Temperature(300, 'K'))
        self.assertEqual(m2.mass_flowrate, prop.MassFlowRate(1, 'ton/h'))

    def test_MaterialStream_instantiation_no_properties(self):
        m3 = MaterialStream()
        self.assertEqual(m3.tag, "MaterialStream_1")
        self.assertEqual(m3.pressure, prop.Pressure())
        self.assertEqual(m3.temperature, prop.Temperature())
        self.assertEqual(m3.mass_flowrate, prop.MassFlowRate())
