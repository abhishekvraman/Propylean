import pytest
import unittest
from propylean.equipments.storages import VerticalStorage
from propylean import properties as prop

class test_VerticalStorage(unittest.TestCase):
    def test_VerticalStorage_representation(self):
        vessel = VerticalStorage(tag="Silo_1")
        self.assertIn("Vertical Storage with tag: Silo_1", str(vessel))
    
    def test_VerticalStorage_blanketing(self):
        v_1 = VerticalStorage(is_blanketed=True, tag="Ethenol_feed_tank")
        v_1.operating_pressure = prop.Pressure(1.5, "atm")
        self.assertEqual(v_1.blanketing.inlet_pressure, prop.Pressure(1.5, "atm"))
        self.assertEqual(v_1.blanketing.outlet_pressure, prop.Pressure(1.5, "atm"))

        self.assertIn("Blanketing with tag: Ethenol_feed_tank_blanketing",
                      str(v_1.blanketing))