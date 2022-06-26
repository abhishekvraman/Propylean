import pytest
import unittest
from propylean.equipments.storages import Bullet
from propylean import properties as prop

class test_Bullet(unittest.TestCase):
    def test_Bullet_representation(self):
        vessel = Bullet(tag="Propane_1")
        self.assertIn("Bullet with tag: Propane_1", str(vessel))
    
    def test_Bullet_blanketing(self):
        v_1 = Bullet(is_blanketed=True, tag="Propylene Storage")
        v_1.operating_pressure = prop.Pressure(1.5, "atm")
        self.assertEqual(v_1.blanketing.inlet_pressure, prop.Pressure(1.5, "atm"))
        self.assertEqual(v_1.blanketing.outlet_pressure, prop.Pressure(1.5, "atm"))

        self.assertIn("Blanketing with tag: Propylene Storage_blanketing",
                      str(v_1.blanketing))