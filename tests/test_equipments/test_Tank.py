import pytest
import unittest
from propylean.equipments.storages import Tank
from propylean import properties as prop

class test_Tank(unittest.TestCase):
    def test_Tank_representation(self):
        vessel = Tank(tag="Caustic Storage tank")
        self.assertIn("Tank with tag: Caustic Storage tank", str(vessel))
    
    def test_Tank_blanketing(self):
        v_1 = Tank(is_blanketed=True, tag="Palm Oil Storage")
        v_1.operating_pressure = prop.Pressure(1.5, "atm")
        self.assertEqual(v_1.blanketing.inlet_pressure, prop.Pressure(1.5, "atm"))
        self.assertEqual(v_1.blanketing.outlet_pressure, prop.Pressure(1.5, "atm"))

        self.assertIn("Blanketing with tag: Palm Oil Storage_blanketing",
                      str(v_1.blanketing))