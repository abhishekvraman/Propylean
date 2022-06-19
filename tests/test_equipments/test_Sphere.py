import pytest
import unittest
from propylean.equipments.storages import Sphere
from propylean import properties as prop

class test_Sphere(unittest.TestCase):
    def test_Sphere_representation(self):
        vessel = Sphere(tag="TKS-4555")
        self.assertIn("Sphere with tag: TKS-4555", str(vessel))
    
    def test_Sphere_blanketing(self):
        v_1 = Sphere(is_blanketed=True, tag="Propylene Export Storage")
        v_1.operating_pressure = prop.Pressure(1.5, "atm")
        self.assertEqual(v_1.blanketing.inlet_pressure, prop.Pressure(1.5, "atm"))
        self.assertEqual(v_1.blanketing.outlet_pressure, prop.Pressure(1.5, "atm"))

        self.assertIn("Blanketing with tag: Propylene Export Storage_blanketing",
                      str(v_1.blanketing))