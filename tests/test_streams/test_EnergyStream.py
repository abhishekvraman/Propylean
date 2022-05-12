import pytest
import unittest

from thermo import Mixture
from propylean.streams import EnergyStream
import propylean.properties as prop
import pandas as pd

class test_EnergyStream(unittest.TestCase):
    @pytest.mark.positive
    def test_EnergyStream_instantiation_tag_only(self):
        e1 = EnergyStream(tag="e1")
        self.assertEqual(e1.tag, "e1")
        self.assertEqual(e1.amount, prop.Power(0, 'W'))
    
    @pytest.mark.positive
    def test_EnergyStream_instantiation_all_base_properties(self):
        e2 = EnergyStream(tag="e2", amount=(10, 'kW'))
        self.assertEqual(e2.amount, prop.Power(10, 'kW'))
    
    @pytest.mark.positive
    def test_EnergyStream_instantiation_no_base_properties(self):
        e3 = EnergyStream()
        self.assertIn("EnergyStream_", e3.tag)
    
    @pytest.mark.positive
    def test_EnergyStream_object_representation(self):
        e4 = EnergyStream(tag="Pump_Inlet_Energy_1")
        self.assertEqual("Energy Stream Tag: Pump_Inlet_Energy_1",str(e4))
